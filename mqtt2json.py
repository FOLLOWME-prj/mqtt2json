import os
import paho.mqtt.client as mqtt
import pandas as pd
from datetime import datetime
import signal
import json
import base64

from gw import gw_pb2
from google.protobuf.json_format import MessageToJson

from chirpstack_window_module import summarize_chirpstack_windows

print("[BOOT] mqtt2json starting (version with SIGTERM->KeyboardInterrupt)")

# ---------------------------
# MQTT Broker settings
# ---------------------------

windowseconds = int(os.getenv("WINDOW_SECONDS"))
print("window seconds : " , windowseconds)
# MQTT_BROKER must be provided via environment variable.
# Example in docker-compose.yml:
#   environment:
#     MQTT_BROKER: "10.0.0.5"
#     MQTT_PORT: "1883"
mqtt_broker_env = os.getenv("MQTT_BROKER")
if not mqtt_broker_env:
    raise RuntimeError(
        "MQTT_BROKER environment variable is not set. "
        "Set it in docker-compose.yml under services.mqtt2json.environment.MQTT_BROKER."
    )

MQTT_BROKER = mqtt_broker_env.strip()
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

# Optional username/password (also via env)
USERMQTT = os.getenv("MQTT_USERNAME_DEFAULT", "")
PASSWORDMTT = os.getenv("MQTT_PASSWORD_DEFAULT", "")

MQTT_USERNAME = os.getenv("MQTT_USERNAME", USERMQTT)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", PASSWORDMTT)


# ---------------------------
# Topics configuration (topics.txt)
# ---------------------------

def load_topics_from_file(path: str):
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
# Output configuration
# ---------------------------
OUTPUT_DIR = "Data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

csv_file_name = os.path.join(OUTPUT_DIR, f"mqtt_data_{RUN_ID}.csv")
jsonl_file_name = os.path.join(OUTPUT_DIR, f"mqtt_data_{RUN_ID}.jsonl")

data_records = []
FLUSH_EVERY = 1000

# ---------------------------
# LoRaWAN helpers
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
    try:
        raw = base64.b64decode(phy_payload_b64)
        if not raw:
            return None, None
        mhdr = raw[0]
        mtype = (mhdr & 0b11100000) >> 5
        name = M_TYPE_NAMES.get(mtype, f"Unknown({mtype})")
        return mtype, name
    except Exception as e:
        print(f"[WARN] Failed to decode PHYPayload for MType: {e}")
        return None, None

def b64_to_reversed_hex(b64_str: str, start: int, length: int) -> str:
    raw = base64.b64decode(b64_str)
    chunk = raw[start:start + length]
    return chunk[::-1].hex() if chunk else ""

def extract_lorawan_fields(decoded_payload):
    if not isinstance(decoded_payload, dict):
        return None, None, None, None

    phy_b64 = None

    # 1) Direct PHYPayload on top-level (e.g., MQTT integration uplink)
    if "phy_payload" in decoded_payload:
        phy_b64 = decoded_payload.get("phy_payload")
    elif "phyPayload" in decoded_payload:
        phy_b64 = decoded_payload.get("phyPayload")

    # 2) Wrapped UplinkFrame (protobuf gw.UplinkFrame)
    if not phy_b64:
        uplink = decoded_payload.get("uplink_frame") or decoded_payload.get("uplinkFrame")
        if isinstance(uplink, dict):
            phy_b64 = uplink.get("phy_payload") or uplink.get("phyPayload")

    # 3) DownlinkFrame with items[] (protobuf gw.DownlinkFrame)
    if not phy_b64:
        items = decoded_payload.get("items")
        if isinstance(items, list) and items:
            first_item = items[0]
            if isinstance(first_item, dict):
                phy_b64 = first_item.get("phy_payload") or first_item.get("phyPayload")

    # If we still don't have a PHYPayload, give up.
    if not phy_b64 or not isinstance(phy_b64, str):
        return None, None, None, None

    # Decode MType
    mtype, mtype_name = get_lorawan_mtype(phy_b64)

    app_eui = None
    dev_eui = None
    dev_addr = None

    # Join-request (uplink): AppEUI + DevEUI
    if mtype_name == "Join-request":
        try:
            app_eui = b64_to_reversed_hex(phy_b64, start=1, length=8)
            dev_eui = b64_to_reversed_hex(phy_b64, start=9, length=8)
        except Exception as e:
            print(f"[WARN] Failed to extract AppEUI/DevEUI: {e}")

    # Data UP (uplink) frames: DevAddr
    if mtype_name in ("Unconfirmed data up", "Confirmed data up"):
        try:
            dev_addr = b64_to_reversed_hex(phy_b64, start=1, length=4)
        except Exception as e:
            print(f"[WARN] Failed to extract DevAddr: {e}")

    return mtype_name, app_eui, dev_eui, dev_addr

# ---------------------------
# Payload decoding
# ---------------------------

def decode_payload(payload):
    try:
        payload_str = payload.decode("utf-8")
        return json.loads(payload_str)
    except Exception:
        pass

    for proto_type in (gw_pb2.UplinkFrame, gw_pb2.DownlinkFrame):
        try:
            msg = proto_type()
            msg.ParseFromString(payload)
            return json.loads(
                MessageToJson(msg, preserving_proto_field_name=True)
            )
        except Exception:
            continue

    return repr(payload)

# ---------------------------
# MQTT callbacks
# ---------------------------

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic, qos)
        print(f"Subscribed to topic: {topic} with QoS {qos}")

def on_message(client, userdata, msg):
    decoded = decode_payload(msg.payload)
    print(decoded)

    topic_parts = msg.topic.split('/')
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

    rssi = None
    spreading_factor = None

    if isinstance(decoded, dict):

        # RSSI

        rx_info = decoded.get("rx_info") or decoded.get("rxInfo")
        if isinstance(rx_info, dict):
            rssi = rx_info.get("rssi")
        elif isinstance(rx_info, list) and rx_info and isinstance(rx_info[0], dict):
            rssi = rx_info[0].get("rssi")


        # Spreading factor

        tx_info = decoded.get("tx_info") or decoded.get("txInfo")
        if isinstance(tx_info, dict):
            modulation = tx_info.get("modulation")
            if isinstance(modulation, dict):
                lora = modulation.get("lora") or modulation.get("LoRa")
                if isinstance(lora, dict):
                    spreading_factor = (
                        lora.get("spreading_factor")
                        or lora.get("spreadingFactor")
                    )


    # If SF == 11 => "Cyber_Attack", else ""
    cyber_attack_msg = "Cyber_Attack" if str(spreading_factor) == "11" else ""

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
        #"RSSI": rssi,
        #"spreading_factor": spreading_factor,
        #"Cyber_Attack": cyber_attack_msg,  
        "payload": json.dumps(decoded, ensure_ascii=False),
    }

    data_records.append(record)

    with open(jsonl_file_name, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    if len(data_records) >= FLUSH_EVERY:
        print(f"Flushing {len(data_records)} records to disk...")
        df = pd.DataFrame(data_records)
        file_exists = os.path.exists(csv_file_name)
        df.to_csv(csv_file_name, index=False, mode="a", header=not file_exists)
        data_records.clear()
        print(f"Appended batch to {csv_file_name}")


# ---------------------------
# Signal handling
# ---------------------------

def handle_sigterm(signum, frame):
    """
    Docker sends SIGTERM (15) on 'docker stop' / 'docker compose down'.
    Convert this into KeyboardInterrupt so we hit the 'finally' block.
    """
    print(f"\n[INFO] Received SIGTERM ({signum}), raising KeyboardInterrupt for graceful shutdown...")
    raise KeyboardInterrupt()

signal.signal(signal.SIGTERM, handle_sigterm)

# ---------------------------
# Main
# ---------------------------

def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"[BOOT] Using broker {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("[INFO] KeyboardInterrupt / SIGTERM received, shutting down...")
    finally:
        # Final flush
        if data_records:
            df = pd.DataFrame(data_records)
            file_exists = os.path.exists(csv_file_name)
            df.to_csv(csv_file_name, index=False, mode="a", header=not file_exists)
            print(f"[FINALIZE] Appended {len(data_records)} records to {csv_file_name}")
        else:
            print("[FINALIZE] No buffered records to flush.")

        # Generate summary if CSV exists
        if os.path.exists(csv_file_name):
            try:
                summary_path = summarize_chirpstack_windows(csv_file_name, window_seconds = windowseconds)
                print(f"[FINALIZE] Summary CSV generated: {summary_path}")
            except Exception as e:
                print(f"[WARN] Failed to generate summary CSV: {e}")
        else:
            print(f"[FINALIZE] CSV file {csv_file_name} does not exist, no summary created.")

        try:
            client.disconnect()
        except Exception:
            pass
        print("[FINALIZE] mqtt2json stopped cleanly.")

if __name__ == "__main__":
    main()
