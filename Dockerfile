FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for pandas & protobuf if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL project files (including gw/, mqtt2json.py, chirpstack_window_module.py, topics.txt, etc.)
COPY . .

# Ensure Data dir exists in image (also mapped as volume)
RUN mkdir -p /app/Data

CMD ["python", "mqtt2json.py"]
