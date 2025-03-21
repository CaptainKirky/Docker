# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.11-bookworm
# FROM python:3.11-bookworm


# Copy the Python Script to blink LED
WORKDIR /app
COPY . /app/

# Intall the rpi.gpio python module
RUN pip install --no-cache-dir rpi.gpio
RUN pip install --no-cache-dir board
# RUN pip install --no-cache-dir adafruit-circuitpython-neopixel
RUN pip install --no-cache-dir rpi_ws281x
RUN pip install --no-cache-dir paho-mqtt
RUN pip install --no-cache-dir suntime

# Trigger Python script
ENTRYPOINT ["python3", "./ledstrip.py"]


