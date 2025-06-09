import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime
import signal
import sys

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
            # Ignore empty comment lines
            return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except Exception as e:
        print(f"Could not load topics from {topics_file}: {e}")
        # Default ChirpStack topics if file is empty
        return ["application/#", "gateway/#"]

def save_data_and_exit(sig, frame):
    print("\nExiting. Data saved to", log_file_name)
    sys.exit(0)

signal.signal(signal.SIGINT, save_data_and_exit)

def on_connect(client, userdata, flags, rc):
    topics = load_topics(TOPICS_FILE)
    print("Connected with result code", rc)
    for topic in topics: client.subscribe(topic)

def on_message(client, userdata, msg):
    print(type(msg.payload))
    payload_str = msg.payload.decode('utf-8', errors='replace').strip()
    # Try to pretty-print as JSON (remove whitespace issues, etc)
    try:
        payload_json = json.loads(payload_str)
        payload_to_write = json.dumps(payload_json, separators=(',', ':'))  # Compact
    except Exception:
        # If not valid JSON, just write the raw string
        payload_to_write = payload_str
    
    print(payload_to_write)
    # Append to log file, each message in new line
    with open(log_file_name, "a", encoding="utf-8") as f:
        f.write(payload_to_write + "\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60) 
client.loop_forever()
