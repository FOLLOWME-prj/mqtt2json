FROM python:3.11-slim

WORKDIR /app

# Copy your python app and proto folders
COPY mqtt2json.py .
COPY requirements.txt .
COPY topics.txt .
COPY gw ./gw
COPY common ./common

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "mqtt2json.py"]



