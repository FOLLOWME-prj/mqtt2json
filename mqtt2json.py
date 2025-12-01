import os
import sys
import paho.mqtt.client as mqtt
import pandas as pd
from datetime import datetime
import signal
import json
import base64

from gw import gw_pb2
from google.protobuf.json_format import MessageToJson


# ----------  MQTT Broker settings (defaults) ----------
MQTT_BROKER_Enter = "192.168.230.1"
MQTT_PORT_Enter = 1883

USERMQTT = ""
PASSWORDMTT = ""

# Broker & credentials (env first, then fallbacks)
MQTT_BROKER   = os.getenv("MQTT_BROKER", MQTT_BROKER_Enter).strip()
MQTT_PORT     = int(os.getenv("MQTT_PORT", MQTT_PORT_Enter))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", USERMQTT)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", PASSWORDMTT)

# ---------------------------
# Topics configuration
# ---------------------------

def load_topics_from_file(path: str):
    """
    Load MQTT topics from a text file.

    Format per line:
      topic [qos]

    - 'topic' is required.
    - 'qos' is optional, defaults to 0.
    - Empty lines and lines starting with '#' are ignored.
    """
    topics = []
    if not os.path.exists(path):
        print(f"[WARN] Topics file '{path}' not found. No topics will be loaded.")
        return topics

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            topic = parts[0]
            qos = 0
            if len(parts) > 1:
                try:
                    qos = int(parts[1])
                except ValueError:
                    print(f"[WARN] Invalid QoS in line '{line}', defaulting to 0")

            topics.append((topic, qos))

    return topics


TOPICS_FILE = os.getenv("TOPICS_FILE", "topics.txt")
MQTT_TOPICS = load_topics_from_file(TOPICS_FILE)

print(f"[BOOT] Topics: {MQTT_TOPICS}")
if not MQTT_TOPICS:
    print("[WARN] No topics loaded. Client will connect but will not subscribe to any topic.")


# ---------------------------
# LoRaWAN helpers (MType, EUIs, DevAddr)
# ---------------------------

M_TYPE_NAMES = {
    0: "Join-request",
    1: "Join-accept",
    2: "Unconfirmed data up",
    3: "Unconfirmed data down",
    4: "Confirmed data up",
    5: "Confirmed data down",
    6: "RFU",
    7: "Proprietary",
}

def get_lorawan_mtype(phy_payload_b64: str):
    """Return (mtype_code, mtype_name) from a base64 PHYPayload."""
    try:
        raw = base64.b64decode(phy_payload_b64)
        if not raw:
            return None, None
        mhdr = raw[0]                 # first byte is MHDR
        mtype = (mhdr & 0b11100000) >> 5
        name = M_TYPE_NAMES.get(mtype, f"Unknown({mtype})")
        return mtype, name
    except Exception as e:
        print(f"[WARN] Failed to decode PHYPayload for MType: {e}")
        return None, None

def b64_to_reversed_hex(b64_str: str, start: int, length: int) -> str:
    """Decode base64, slice bytes [start:start+length], reverse, return hex."""
    raw = base64.b64decode(b64_str)
    chunk = raw[start:start + length]
    # LoRaWAN stores many fields LSB-first, so reverse to MSB-first hex
    return chunk[::-1].hex() if chunk else ""

def extract_lorawan_fields(decoded_payload):
    """
    From the decoded JSON dict, extract:
      - MType (code + name)
      - AppEUI, DevEUI for Join-request
      - Device_address for uplink data frames
    Returns: (mtype_name, app_eui, dev_eui, dev_addr)
    """
    if not isinstance(decoded_payload, dict):
        return None, None, None, None

    # Try common locations for phy_payload
    phy_b64 = None
    if "phy_payload" in decoded_payload:
        phy_b64 = decoded_payload.get("phy_payload")
    elif "phyPayload" in decoded_payload:
        phy_b64 = decoded_payload.get("phyPayload")
    else:
        # Sometimes nested (e.g., uplink_frame -> phy_payload)
        uplink = decoded_payload.get("uplink_frame") or decoded_payload.get("uplinkFrame")
        if isinstance(uplink, dict):
            phy_b64 = uplink.get("phy_payload") or uplink.get("phyPayload")

    if not phy_b64 or not isinstance(phy_b64, str):
        return None, None, None, None

    mtype_code, mtype_name = get_lorawan_mtype(phy_b64)
    app_eui = None
    dev_eui = None
    dev_addr = None

    if mtype_name == "Join-request":
        # AppEUI (bytes 1..8), DevEUI (bytes 9..16) – 8 bytes each
        try:
            app_eui = b64_to_reversed_hex(phy_b64, start=1, length=8)
            dev_eui = b64_to_reversed_hex(phy_b64, start=9, length=8)
        except Exception as e:
            print(f"[WARN] Failed to extract AppEUI/DevEUI: {e}")

    # For uplink data frames, extract DevAddr (4 bytes at offset 1)
    if mtype_name in ("Unconfirmed data up", "Confirmed data up"):
        try:
            dev_addr = b64_to_reversed_hex(phy_b64, start=1, length=4)
        except Exception as e:
            print(f"[WARN] Failed to extract DevAddr: {e}")

    return mtype_name, app_eui, dev_eui, dev_addr


# ---------------------------
# Output configuration
# ---------------------------
OUTPUT_DIR = "Data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# One run ID used for both CSV and JSONL filenames
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

csv_file_name = os.path.join(OUTPUT_DIR, f"mqtt_data_{RUN_ID}.csv")
jsonl_file_name = os.path.join(OUTPUT_DIR, f"mqtt_data_{RUN_ID}.jsonl")

data_records = []
FLUSH_EVERY = 1000  # Flush to CSV every N messages


def save_data():
    """Flush accumulated records to the CSV file."""
    if data_records:
        df = pd.DataFrame(data_records)

        # Append to this run's CSV file; write header only if file does not exist yet
        file_exists = os.path.exists(csv_file_name)
        df.to_csv(csv_file_name, index=False, mode="a", header=not file_exists)

        print(f"Appended {len(data_records)} records to {csv_file_name}")
    else:
        print("No data to save.")


def save_data_and_exit(sig, frame):
    print(f"\nReceived signal {sig}. Exiting. Saving data...")
    save_data()
    sys.exit(0)


def maybe_flush():
    """Flush to CSV when we have accumulated enough records."""
    if len(data_records) >= FLUSH_EVERY:
        print(f"Flushing {len(data_records)} records to disk...")
        save_data()
        data_records.clear()


signal.signal(signal.SIGINT, save_data_and_exit)
signal.signal(signal.SIGTERM, save_data_and_exit)


def decode_payload(payload):
    """Decode MQTT payload: try JSON, then protobuf, then raw repr."""
    # 1. Try JSON
    try:
        payload_str = payload.decode("utf-8")
        return json.loads(payload_str)
    except Exception:
        pass

    # 2. Try protobuf types
    for proto_type in (gw_pb2.UplinkFrame, gw_pb2.DownlinkFrame):
        try:
            msg = proto_type()
            msg.ParseFromString(payload)
            return json.loads(
                MessageToJson(msg, preserving_proto_field_name=True)
            )
        except Exception:
            continue

    # 3. Fallback: raw repr
    return repr(payload)


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic, qos)
        print(f"Subscribed to topic: {topic} with QoS {qos}")


def on_message(client, userdata, msg):
    decoded = decode_payload(msg.payload)
    print(decoded)

    topic_parts = msg.topic.split("/")
    device_type = None
    mac = None

    if "gateway" in topic_parts:
        device_type = "gateway"
    elif "device" in topic_parts:
        device_type = "device"

    if device_type and device_type in topic_parts:
        mac_index = topic_parts.index(device_type) + 1
        if mac_index < len(topic_parts):
            mac = topic_parts[mac_index]

    state = topic_parts[-1] if topic_parts else None

    # LoRaWAN-specific fields: MType, AppEUI, DevEUI, Device_address
    mtype_name, app_eui, dev_eui, dev_addr = extract_lorawan_fields(decoded)

    record = {
        "timestamp": datetime.now().isoformat(),
        "topic": msg.topic,
        "device_type": device_type,
        "mac": mac,
        "state": state,
        "MType": mtype_name,
        "AppEUI": app_eui,
        "DevEUI": dev_eui,
        "Device_address": dev_addr,
        "payload": json.dumps(decoded, ensure_ascii=False),
    }

    # Buffer for CSV batching
    data_records.append(record)

    # Append to JSONL stream file (one JSON object per line)
    with open(jsonl_file_name, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    maybe_flush()


# ---------------------------
# MQTT client setup
# ---------------------------
mqttc = mqtt.Client()
mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

print(f"[BOOT] Using broker {MQTT_BROKER}:{MQTT_PORT}")
mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
mqttc.loop_forever()
