FROM python:3.9-slim

# Install mosquitto (MQTT broker)
RUN apt-get update && \
    apt-get install -y mosquitto && \
    apt-get clean

# Install the Python MQTT client library (paho-mqtt)
RUN pip3 install paho-mqtt==1.6.1
RUN pip3 install pycryptodome==3.21.0

# Copy all Python scripts from the local ./src directory to /app/src in the container
COPY ./src /app/src

# Set the working directory to /app/src
WORKDIR /app/src

# Expose port 12345
EXPOSE 12345

# Start mosquitto in the background and then run the main script (run.py)
CMD mosquitto -d && python3 /app/src/scripts/run.py