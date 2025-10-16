# mqtt2json: log MQTT messages in JSON format

This project exports MQTT messages by saving each message as a JSON object.
The logger is designed to run easily in Docker and to work seamlessly with ChirpStack.
By default, it subscribes to the application/# and gateway/# topics, but these can be customized.

## 1. Prerequisites

- An [MQTT](https://mqtt.org) instance (such as the one provided by [ChirpStack](https://www.chirpstack.io)) running
- [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/) installed on your system

## 2. Configure ChirpStack Gateway Bridge to Use JSON

By default, [ChirpStack](https://www.chirpstack.io) encodes uplink and downlink messages in `protobuf` format.
To use this tool as-is, you have two options:

- Option A: Use JSON encoding (simpler)

1. Open the gateway bridge configuration file located in `/etc/chirpstack-gateway-bridge/chirpstack-gateway-bridge.toml`
2. Find the following line:
    ```
    marshaler="protobuf"
    ```
3. Change it to:
    ```
    marshaler="json"
    ```
4. Save and close the file
5. Restart the gateway bridge:
    ```bash
    sudo systemctl restart chirpstack-gateway-bridge
    ```
- Option B: Use protobuf decoding (recommended for full fidelity)
This tool supports protobuf decoding of ChirpStack messages out of the box.
Make sure your mqtt2json.py is configured properly and protobuf Python files are included in the Docker image.
## 3. Configure MQTT Topics

The topics to subscribe to are loaded from the `topics.txt` file, considering the following:

* Each line should be a topic string (wildcards like `#` are supported)

* By default, the file includes the `application` and `gateway` topics (to attach to [ChirpStack](https://www.chirpstack.io) data), although they can be changed easily:

  ```
  application/#
  gateway/#
  ```

* You can add, remove, or comment out lines (lines starting with `#` will be ignored).

**Sample `topics.txt` content:**

```
# ChirpStack default topics
application/#
gateway/#

# Custom topic example
# my/custom/topic
```

## 4. Configure the tool

1. Open `mqtt2json.py` in your editor:
2. Set the `MQTT_BROKER` variable (and, optionally, the `MQTT_PORT` variable accordingly) to your [MQTT](https://mqtt.org) broker address:
    ```python
    MQTT_BROKER = "your.mqtt.broker.ip"
    ```
    Replace `your.mqtt.broker.ip` with your actual broker IP or hostname, for example `127.0.0.1`.
3. Set the USERMQTT and PASSWORDMTT variables based on the username and password of your MQTT broker.
If your broker does not require authentication, leave both variables empty, like this:

USERMQTT = ""
PASSWORDMTT = ""


## 5. Build and run with Docker

Enter the repository folder and run the following commands:
```bash
docker compose build
docker compose up
```

To clean up everything, run the following command:
```bash
docker compose down
```

## 6. Output format

Output is represented by a single line for each message.
Each line in the output file represents a [JSON](https://www.json.org) object.

A sample output can be found in the `output` folder.
