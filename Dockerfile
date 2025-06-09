FROM python:3.11-slim

WORKDIR /app

COPY mqtt2json.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "mqtt2json.py"]
