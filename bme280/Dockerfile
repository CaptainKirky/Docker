# Python Base Image from https://hub.docker.com/r/arm32v7/python/
# FROM arm32v7/python:3.11-bookworm
# FROM arm64v8/python:3.13-bookworm
 FROM arm64v8/python:3.11-bookworm

# Copy the Python Script to blink LED
WORKDIR /app
COPY . /app/

# Intall the rpi.gpio python module

RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir paho-mqtt==1.6.1
RUN pip install --no-cache-dir RPI.BME280

# Trigger Python script
ENTRYPOINT ["python3", "./bme.py"]


