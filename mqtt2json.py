# mqtt2json.py
import os
import sys
import json
import socket
from datetime import datetime

import pandas as pd
import paho.mqtt.client as mqtt
from gw import gw_pb2
from google.protobuf.json_format import MessageToJson


# ----------  MQTT Broker settings (defaults) ----------
MQTT_BROKER_Enter = "your.mqtt.broker.ip"
MQTT_PORT_Enter = 1883

USERMQTT = ""
PASSWORDMTT = ""


# ---------- Config (env overrides; safe defaults) ----------
TOPICS_FILE = os.getenv("TOPICS_FILE", "topics.txt")
OUTPUT_DIR  = os.getenv("OUTPUT_DIR", "Data")

# Broker & credentials (env first, then fallbacks)
MQTT_BROKER   = os.getenv("MQTT_BROKER", MQTT_BROKER_Enter).strip()
MQTT_PORT     = int(os.getenv("MQTT_PORT", MQTT_PORT_Enter))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", USERMQTT)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", PASSWORDMTT)

# Default topics if topics.txt is missing
DEFAULT_TOPICS = [("application/#", 0), ("eu868/gateway/#", 0), ("gateway/#", 0)]

# Optional: stream every message to JSONL
STREAM_JSONL = os.getenv("STREAM_JSONL", "1") == "1"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Use a fixed CSV/JSONL filename (easier to find)
csv_file_name   = os.path.join(OUTPUT_DIR, "mqtt_data.csv")
jsonl_file_name = os.path.join(
    OUTPUT_DIR,
    f"mqtt_stream_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl",
)


# ---------- Helpers ----------
def load_topics(topics_file: str):
    try:
        with open(topics_file, "r", encoding="utf-8") as f:
            topics = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        # Accept "topic [qos]" or just "topic"
        parsed = []
        for line in topics:
            parts = line.split()
            if len(parts) == 1:
                parsed.append((parts[0], 0))
            else:
                t, qos = parts[0], int(parts[1])
                parsed.append((t, qos))
        return parsed or DEFAULT_TOPICS
    except Exception as e:
        print(f"[BOOT] Could not load {topics_file}: {e} — using defaults.")
        return DEFAULT_TOPICS


def decode_payload(payload: bytes):
    # 1) Try JSON
    try:
        payload_str = payload.decode("utf-8")
        return json.loads(payload_str)  # dict/list if JSON
    except Exception:
        pass

    # 2) Try LoRa gateway protobufs
    for proto_type in (gw_pb2.UplinkFrame, gw_pb2.DownlinkFrame):
        try:
            msg = proto_type()
            msg.ParseFromString(payload)
            return json.loads(MessageToJson(msg, preserving_proto_field_name=True))
        except Exception:
            continue

    # 3) Fallback: repr of bytes
    return repr(payload)


def flatten_value_for_csv(v):
    # CSV can store JSON strings for structured payloads
    try:
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        return str(v)


def append_to_csv(record: dict):
    """
    Append a single record to the CSV file.
    Creates the file with header if it doesn't exist yet.
    """
    df = pd.DataFrame([record])

    # Serialize dict/list payloads as JSON string for CSV
    if "payload" in df.columns:
        df["payload"] = df["payload"].apply(flatten_value_for_csv)

    file_exists = os.path.isfile(csv_file_name)
    df.to_csv(csv_file_name, mode="a", header=not file_exists, index=False)


def stream_jsonl(record: dict):
    with open(jsonl_file_name, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# Normalize broker if user accidentally provided a URL
if MQTT_BROKER.startswith(("mqtt://", "tcp://")):
    MQTT_BROKER = MQTT_BROKER.split("://", 1)[1].split("/", 1)[0].strip()

# Early sanity check
try:
    ai = socket.getaddrinfo(MQTT_BROKER, MQTT_PORT)
    print(f"[BOOT] Using broker {MQTT_BROKER}:{MQTT_PORT} (resolves to {ai[0][4]})")
except Exception as e:
    print(f"[BOOT] Name/addr resolution FAILED for {MQTT_BROKER}:{MQTT_PORT}: {e}")
    sys.exit(2)

TOPICS = load_topics(TOPICS_FILE)
print(f"[BOOT] Topics: {TOPICS}")
print(f"[BOOT] Output dir: {OUTPUT_DIR}")
print(f"[BOOT] Auth user set: {'yes' if MQTT_USERNAME else 'no'}")


# ---------- MQTT callbacks (Paho v2) ----------
def on_connect(client, userdata, flags, reasonCode, properties=None):
    print(f"[CONNECT] code={reasonCode}")
    for topic, qos in TOPICS:
        client.subscribe(topic, qos)
        print(f"[SUB] {topic} (QoS {qos})")


def on_message(client, userdata, msg):
    decoded = decode_payload(msg.payload)

    topic_parts = msg.topic.split("/")
    device_type = "gateway" if "gateway" in topic_parts else ("device" if "device" in topic_parts else None)
    mac = None
    if device_type and device_type in topic_parts:
        i = topic_parts.index(device_type) + 1
        if i < len(topic_parts):
            mac = topic_parts[i]
    state = topic_parts[-1] if topic_parts else None

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "topic": msg.topic,
        "device_type": device_type,
        "mac": mac,
        "state": state,
        "payload": decoded,
    }

    # Write to CSV immediately
    append_to_csv(record)

    # Optional JSONL streaming
    if STREAM_JSONL:
        stream_jsonl(record)

    # Console output
    print(f"[MSG] {msg.topic} | MAC={mac} | State={state} | len={len(msg.payload)}")


# ---------- Connect & loop ----------
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if MQTT_USERNAME or MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

print(f"[CONNECTING] {MQTT_BROKER}:{MQTT_PORT} (auth={'yes' if MQTT_USERNAME else 'no'})")
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_forever()
