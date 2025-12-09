mqtt2json: Log MQTT Messages in JSON and CSV Format


This project subscribes to MQTT topics and logs all received messages
into structured files (CSV and JSON). It is designed to run easily
inside Docker and integrates seamlessly with ChirpStack.

By default, it subscribes to ChirpStack application and gateway topics,
decodes LoRaWAN frames, extracts metadata such as MType, DevEUI,
DevAddr, and automatically generates time-window summaries.

  -------------------------
  1. Clone the Repository
  -------------------------

git clone https://github.com/FOLLOWME-prj/mqtt2json.git cd mqtt2json

  ------------------
  2. Prerequisites
  ------------------

-   A running MQTT Broker (for example from ChirpStack)
-   Docker
-   Docker Compose

  -----------------------------------------------------------
  3. Configure ChirpStack Gateway Bridge (JSON or Protobuf)
  -----------------------------------------------------------

Option A: Use JSON Encoding (Simpler)

sudo nano /etc/chirpstack-gateway-bridge/chirpstack-gateway-bridge.toml

Change: marshaler=“protobuf”

To: marshaler=“json”

Restart: sudo systemctl restart chirpstack-gateway-bridge

Option B: Use Protobuf Encoding (Recommended) No changes required. This
project supports protobuf decoding.

  --------------------------
  4. Configure MQTT Topics
  --------------------------

topics.txt default content:

application/# gateway/#

  ------------------------------
  5. Configure Docker Settings
  ------------------------------

nano docker-compose.yml

Modify:

MQTT_BROKER: “172.17.73.34” MQTT_PORT: “1883” MQTT_USERNAME: “”
MQTT_PASSWORD: “” WINDOW_SECONDS: “55”

  ------------------------------
  6. Build and Run the Project
  ------------------------------

sudo docker compose build sudo docker compose up

To stop:

sudo docker compose down

  -----------------------------------------
  7. Output Files (Saved in Data/ Folder)
  -----------------------------------------

1.  Raw CSV of MQTT messages
2.  Window summary CSV
3.  JSONL file (one JSON object per line)

<<<<<<< Updated upstream
  ---------------------
  8. Features Summary
  ---------------------
=======
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

| timestamp           | topic                      | device_type | mac         | state     |MType       |AppEUI    |DevEUI    |Device_address| payload           |
|---------------------|----------------------------|-------------|-------------|-----------| -----------| ---------| ---------| -------------|-------------------|
| 2025-08-06 13:00:00 | application/device/xxx/tx  | device      | abcd1234    | tx        | JoinRequest| abcd1234 | 00000    | adr01        | {...decoded...}   |
| ...                 | ...                        | ...         | ...         | ...       | ....       | ....     | ....     | ....         | ...               |

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
>>>>>>> Stashed changes

-   MQTT live subscription
-   ChirpStack integration
-   Protobuf & JSON decoding
-   LoRaWAN MType decoding
-   CSV + JSONL logging
-   Time-window aggregation
-   Fully Dockerized
-   Window configurable via Docker
