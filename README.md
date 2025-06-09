# mqtt2json: log MQTT messages in JSON format

This project exports [MQTT](https://mqtt.org) messages, saving each message as a [JSON](https://www.json.org) object.
The logger is designed to run easily in [Docker](https://www.docker.com) and to use it with [ChirpStack](https://www.chirpstack.io).

This version has been enhanced to **automatically detect and decode both `json` and `protobuf`** message formats from ChirpStack topics.

## 1. Prerequisites

- An [MQTT](https://mqtt.org) instance (such as the one provided by [ChirpStack](https://www.chirpstack.io)) running.
- [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/) installed on your system.

## 2. Automatic Format Handling (JSON & Protobuf)

This tool supports both `json` and `protobuf` marshalers automatically, using the default ChirpStack configuration.

* You can add, remove, or comment out lines (lines starting with `#` will be ignored).

**Sample `topics.txt` content:**

```
# ChirpStack default topics
application/#
gateway/#

# Custom topic example
# my/custom/topic
```

You **no longer need to modify** the `chirpstack-gateway-bridge.toml` file. The script handles both formats out of the box, converting everything into a consistent JSON output.

## 3. Configure MQTT Topics

The topics to subscribe to are loaded from the `topics.txt` file.

* Each line should be a topic string (wildcards like `#` are supported).
* Lines starting with `#` will be ignored.
* By default, the file includes the `application/#` and `gateway/#` topics for ChirpStack.

**Sample `topics.txt` content:**