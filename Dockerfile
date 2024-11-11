# FROM debian:latest

# RUN apt-get update && \
#     apt-get install -y \
#     mosquitto \
#     python3 \
#     python3-pip \
#     python3-dev \
#     build-essential \
#     && apt-get clean

# RUN python3 -m pip install --upgrade pip

# RUN pip3 install paho-mqtt

# COPY ./src /app/src

# WORKDIR /app/src

# EXPOSE 12345

# CMD mosquitto -d && python3 /app/src/scripts/run.py

FROM python:3.9-slim

# Install mosquitto (MQTT broker)
RUN apt-get update && \
    apt-get install -y mosquitto && \
    apt-get clean

# Install the Python MQTT client library (paho-mqtt)
RUN pip3 install paho-mqtt==1.6.1

# Copy all Python scripts from the local ./src directory to /app/src in the container
COPY ./src /app/src

# Set the working directory to /app/src
WORKDIR /app/src

# Expose port 12345
EXPOSE 12345

# Start mosquitto in the background and then run the main script (run.py)
CMD mosquitto -d && python3 /app/src/scripts/run.py