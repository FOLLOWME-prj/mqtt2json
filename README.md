# MQTT2JSON

![MQTT Architecture](mqtt_architecture.png)

This project subscribes to MQTT topics and logs all received messages
into structured files (CSV and JSON). It is designed to run easily
inside Docker and integrates seamlessly with ChirpStack.

By default, it subscribes to ChirpStack application and gateway topics,
decodes LoRaWAN frames, extracts metadata such as MType, DevEUI,
DevAddr, and automatically generates time-window summaries.


# Installation


### 1) Clone the repository and enter the folder:

```bash
git clone https://github.com/FOLLOWME-prj/mqtt2json.git
```
```bash
cd mqtt2json
```

### 2) Configure ChirpStack Gateway Bridge (JSON or Protobuf)

Option A: Use JSON Encoding (Simpler)
This option decodes the messages to JSON.

Open the ChirpStack Gateway Bridge configuration file:
```bash
sudo nano /etc/chirpstack-gateway-bridge/chirpstack-gateway-bridge.toml
```
Find the marshaler setting and change:

marshaler = "protobuf"

to:

marshaler = "json"

Restart the service:
```bash
sudo systemctl restart chirpstack-gateway-bridge
```

Option B: Use Protobuf Encoding
No changes required. This project supports Protobuf decoding.



# Configuration


### 1) Update topics.txt

Edit topics.txt and set the MQTT topics based on your network configuration.

Example topics:
application/#
gateway/#


### 2) Update docker-compose.yml

Open docker-compose.yml:
```bash
nano docker-compose.yml
```
Modify the broker and port:

MQTT_BROKER: "172.17.73.34"
MQTT_PORT: "1883"

If MQTT authentication is used, set username and password. If not, leave empty:

MQTT_USERNAME: ""
MQTT_PASSWORD: ""

Choose the capture time window (seconds):

WINDOW_SECONDS: "55"



# Execution


Run the project using Docker Compose:
```bash
sudo docker compose up
```
After getting enough data, stop the program using:

CTRL + C

The captured data is saved in the Data folder.
Messages are saved in two formats: JSON and CSV.
A CSV file is also generated containing the number of Join Requests and Uplinks
captured per configured time window.





