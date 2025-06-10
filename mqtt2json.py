import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import signal
from gw import gw_pb2
from google.protobuf.json_format import MessageToJson
import paho.mqtt.client as mqtt
import json
from datetime import datetime


# Generic settings
TOPICS_FILE = "topics.txt"
OUTPUT_DIR = "output"

# MQTT broker settings
MQTT_BROKER = "your.mqtt.broker.ip"
MQTT_PORT = 1883

os.makedirs(OUTPUT_DIR, exist_ok=True)
log_file_name = os.path.join(OUTPUT_DIR, f"mqtt_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def load_topics(topics_file):
    try:
        with open(topics_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except Exception as e:
        print(f"Could not load topics from {topics_file}: {e}")
        return ["application/#", "gateway/#"]

def save_data_and_exit(sig, frame):
    print("\nExiting. Data saved to", log_file_name)
    sys.exit(0)

signal.signal(signal.SIGINT, save_data_and_exit)

def on_connect(client, userdata, flags, rc):
    topics = load_topics(TOPICS_FILE)
    print("Connected with result code", rc)
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Received message on topic: {msg.topic}, payload length: {len(msg.payload)}")

    # Try JSON decode
    try:
        payload_str = msg.payload.decode('utf-8', errors='strict').strip()
        try:
            payload_json = json.loads(payload_str)
            payload_to_write = json.dumps(payload_json, separators=(',', ':'))
            print("Received JSON payload")
        except Exception:
            raise ValueError("Not JSON, try protobuf")
    except Exception:
        payload_str = None

    if payload_str is None or 'payload_to_write' not in locals():
        # Try protobuf decode(s)
        decode_success = False
        for proto_type in [gw_pb2.UplinkFrame, gw_pb2.DownlinkFrame]:  # Add more types if needed
            try:
                proto_msg = proto_type()
                proto_msg.ParseFromString(msg.payload)
                payload_to_write = MessageToJson(proto_msg, preserving_proto_field_name=True)
                print(f"Received protobuf payload of type: {proto_type.__name__}")
                decode_success = True
                break
            except Exception as e:
                # Try next proto type
                continue

        if not decode_success:
            print(f"Failed to decode payload as JSON or protobuf.")
            print(f"Raw payload bytes (first 50): {msg.payload[:50]}")
            payload_to_write = "<Could not decode payload as JSON or protobuf>"

            # Optionally save unknown payload to file for offline analysis
            unknown_file = os.path.join(OUTPUT_DIR, "unknown_payloads.bin")
            with open(unknown_file, "ab") as f:
                f.write(msg.payload + b"\n---\n")

    print(payload_to_write)
    with open(log_file_name, "a", encoding="utf-8") as f:
        f.write(payload_to_write + "\n")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
