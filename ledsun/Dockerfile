# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.11-bookworm

# Copy the Python Script to blink LED
WORKDIR /app
COPY . /app/

# Intall the rpi.gpio python module
RUN pip install --no-cache-dir rpi.gpio
RUN pip install --no-cache-dir suntime
RUN pip install --no-cache-dir datetime

# Trigger Python script
ENTRYPOINT ["python3", "./led13sun.py"]


