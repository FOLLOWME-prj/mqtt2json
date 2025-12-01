# Capture Data

A Python-based MQTT data capture tool for subscribing to MQTT topics, decoding JSON and Protobuf payloads, and saving structured data for analysis.  
Ideal for IoT, LoRaWAN, or any MQTT-based system.

---

## Features

- Connects to an MQTT broker (local or remote)
- Subscribes to custom topics (supports wildcards)
- Decodes:
  - JSON
  - Google Protocol Buffers (Protobuf)
  - Raw binary data (as fallback)
- Extracts device information from topics (e.g., MAC, device type, state)
- Saves results as CSV for easy analysis

---

## Requirements

- Python 3.8+
- MQTT broker accessible on your network (e.g., [Eclipse Mosquitto](https://mosquitto.org/))
- Access to relevant `.proto` files for Protobuf decoding (if used)
- Python packages:
  - `paho-mqtt`
  - `pandas`
  - `protobuf`
  - (optional) `google.protobuf.json_format` for Protobuf JSON export

---

## Installation

1. **Clone this repository:**
    ```sh
    git clone https://github.com/yourusername/capture-data.git
    cd capture-data
    ```

2. **Install required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```
    Or manually:
    ```sh
    pip install paho-mqtt pandas protobuf
    ```

3. **(If using Protobuf) Generate Python files from `.proto` definitions:**
    ```sh
    # Make sure you have protoc installed (version must match your Python protobuf)
    # Example:
    protoc --proto_path=. --python_out=. gw/gw.proto
    protoc --proto_path=. --python_out=. common/common.proto
    ```
    - Ensure all generated `_pb2.py` files are present in the repo.

---

## Configuration

1. **Set MQTT broker address and port in your script:**
    ```python
    MQTT_BROKER = "192.168.230.1"   # Change to your broker's IP or hostname
    MQTT_PORT = 1883                # Change to your broker's port if different
    ```
2. **Set your topic filters:**
    ```python
    MQTT_TOPICS = [("application/#", 0), ("eu868/gateway/#", 0), ("gateway/#", 0)]
    ```
    - Adjust topics as needed for your environment.

3. **Protobuf Decoding (optional):**
    - If your payloads use Protobuf, make sure you have the relevant `.proto` files.
    - Regenerate `_pb2.py` after any changes to the `.proto` files or when changing Protobuf versions.

---

## How to Connect to the Network

1. **Ensure your MQTT broker is running and reachable:**
    - If running locally: `localhost` or `127.0.0.1`
    - If on another device: Use that device’s IP (e.g., `192.168.230.1`)
    - If using a cloud broker: Use the DNS/host and port provided

2. **Test network access:**
    - From your client machine:
        ```sh
        ping 192.168.230.1
        ```
    - Test MQTT connection using an MQTT client (e.g., [MQTT Explorer](https://mqtt-explorer.com/) or [mosquitto_sub](https://mosquitto.org/)):
        ```sh
        mosquitto_sub -h 192.168.230.1 -t "#" -v
        ```
    - If you get a response, your network connection is good.

3. **Firewall and Broker Configuration:**
    - Ensure that TCP port `1883` (or the port you use) is open on the broker host.
    - Broker must be configured to listen on the desired interface (not just `localhost`).

4. **Authentication (if required):**
    - If your broker uses usernames/passwords or TLS, add them in the Python script:
        ```python
        mqttc.username_pw_set("username", "password")
        # For TLS/SSL
        mqttc.tls_set(ca_certs="path/to/ca.crt")
        ```

---

## Usage

1. **Start the script:**
    ```sh
    python Capture\ Data.py
    ```

2. **On receiving MQTT messages:**
    - Decoded payloads and topic details are displayed.
    - Data is stored in memory until you exit.

3. **To stop and save:**
    - Press `Ctrl+C` in the terminal or command prompt.
    - The script will save all captured data as a CSV file in the `mqtt_logs` directory, with a timestamped filename.

---

## Troubleshooting

- **Cannot connect to MQTT broker?**
    - Check broker is running and listening on the correct IP/port.
    - Ensure no firewall is blocking port `1883`.
    - Double-check IP addresses and network settings.

- **Protobuf errors?**
    - Make sure you’re using matching versions of `protoc` and `protobuf` Python library.
    - Regenerate `_pb2.py` files with the correct version of `protoc`.

- **Can’t decode payload?**
    - If not JSON or Protobuf, raw binary will be stored for offline analysis.

- **Still stuck?**
    - Try connecting with a third-party MQTT client (MQTT Explorer, mosquitto_sub).
    - Check your broker logs for errors.

---

## Example Output

Captured data is stored as a CSV file like this:

| timestamp           | topic                      | device_type | mac         | state     | payload           |
|---------------------|----------------------------|-------------|-------------|-----------|-------------------|
| 2025-08-06 13:00:00 | application/device/xxx/tx  | device      | abcd1234    | tx        | {...decoded...}   |
| ...                 | ...                        | ...         | ...         | ...       | ...               |

---

## Contributing

Feel free to open issues or submit pull requests!

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- [paho-mqtt](https://pypi.org/project/paho-mqtt/)
- [protobuf](https://pypi.org/project/protobuf/)
- [Pandas](https://pandas.pydata.org/)
- Your MQTT broker of choice

---

## Questions?

Open an issue or contact [TareghKhanjari@CNR.it].

