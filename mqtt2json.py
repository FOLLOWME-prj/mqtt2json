import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime
import signal
import sys
import re
import base64

# Protobuf Imports 
PROTOBUF_AVAILABLE = False
try:
    from chirpstack_api.gw import gw_pb2
    from google.protobuf.json_format import MessageToDict
    from google.protobuf.message import DecodeError as ProtobufDecodeError
    PROTOBUF_AVAILABLE = True
    print("Successfully imported Protobuf modules.")
except ImportError:
    print("WARNING: Could not import Protobuf modules. Gateway message decoding will be limited.")
    # Create a dummy exception class if protobuf is not available for clean error handling
    class ProtobufDecodeError(Exception): pass

# Configuration 
TOPICS_FILE = "topics.txt"
OUTPUT_DIR = "output"
MQTT_BROKER = "10.20.80.155"  # SET YOUR BROKER IP HERE
MQTT_PORT = 1883

# Setup output directory and log file name 
os.makedirs(OUTPUT_DIR, exist_ok=True)
log_file_name = os.path.join(OUTPUT_DIR, f"mqtt_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
print(f"Logging data to: {log_file_name}")


def convert_keys_to_camel_case(item):
    """
    Recursively converts dictionary keys.
    """
    if isinstance(item, dict):
        new_dict = {}
        for k, v in item.items():
            new_key = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), k)
            new_dict[new_key] = convert_keys_to_camel_case(v)
        return new_dict
    elif isinstance(item, list):
        return [convert_keys_to_camel_case(i) for i in item]
    return item


def load_topics(topics_file):
    try:
        with open(topics_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except Exception as e:
        print(f"Could not load topics from {topics_file}: {e}")
        # Default to standard ChirpStack topics if file is missing
        return ["application/#", "gateway/#"]

def save_data_and_exit(sig, frame):
    print("\nExiting. Data saved to", log_file_name)
    sys.exit(0)

signal.signal(signal.SIGINT, save_data_and_exit)

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    """
    Callback for when the client connects to the MQTT broker.
    Subscribes to topics loaded from the topics.txt file.
    """
    if rc == 0:
        print(f"Connected successfully to MQTT Broker: {MQTT_BROKER}")
        topics = load_topics(TOPICS_FILE)
        print(f"Subscribing to topics: {topics}")
        for topic in topics:
            client.subscribe(topic)
    else:
        print(f"Failed to connect. Return code: {rc}")

def on_message(client, userdata, msg):
    """
    Callback for when a message is received.
    Auto-detects format (JSON or Protobuf) based on topic.
    """
    payload_bytes = msg.payload
    final_dict = None

    # Handle application topics (which use JSON)
    if msg.topic.startswith("application/"):
        try:
            final_dict = json.loads(payload_bytes.decode('utf-8'))
        except json.JSONDecodeError:
            print(f"WARN: Could not decode JSON on app topic: {msg.topic}")
            return 

    # Handle gateway topics (which use Protobuf)
    elif msg.topic.startswith("gateway/") and PROTOBUF_AVAILABLE:
        topic_parts = msg.topic.split('/')
        event_type = topic_parts[-1] if len(topic_parts) > 1 else ""
        
        proto_class = None
        if event_type == "up": proto_class = gw_pb2.UplinkFrame
        elif event_type == "stats": proto_class = gw_pb2.GatewayStats
        elif event_type == "down": proto_class = gw_pb2.DownlinkFrame
        elif event_type == "ack":
            proto_class = getattr(gw_pb2, 'DownlinkTxAck', getattr(gw_pb2, 'DownlinkTXAck', None))

        if proto_class:
            try:
                proto_message = proto_class()
                proto_message.ParseFromString(payload_bytes)
                snake_case_dict = MessageToDict(
                    proto_message,
                    preserving_proto_field_name=True,
                    including_default_value_fields=True
                )
                final_dict = convert_keys_to_camel_case(snake_case_dict)
            except ProtobufDecodeError:
                print(f"WARN: Protobuf decode failed on topic: {msg.topic}")
                return 

   
    if final_dict:
        try:
            output_line = json.dumps(final_dict, separators=(',', ':'))
            with open(log_file_name, "a", encoding="utf-8") as f:
                f.write(output_line + "\n")
            print(f"Logged message from topic: {msg.topic}")
        except Exception as e:
            print(f"ERROR: Failed to write to log file: {e}")


print("Initializing MQTT client...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"Attempting to connect to MQTT Broker at {MQTT_BROKER}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Starting MQTT client loop. Press Ctrl+C to stop.")
    client.loop_forever()
except KeyboardInterrupt:
    save_data_and_exit(None, None)
except Exception as e:
    print(f"CRITICAL: An error occurred. Error: {e}")
    sys.exit(1)