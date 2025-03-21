# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.11-bookworm

# Copy the Python Script to blink LED
WORKDIR /app
COPY . /app/

# Intall the rpi.gpio python module
RUN pip install --no-cache-dir Adafruit_GPIO
RUN pip install --no-cache-dir paho-mqtt==1.6.1
RUN pip install --no-cache-dir Adafruit_SSD1306
RUN pip install --no-cache-dir pillow
RUN pip install --no-cache-dir rpi.gpio


# Trigger Python script
ENTRYPOINT ["python3", "./LEDDisplay.py"]


