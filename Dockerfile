FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
        mosquitto \
        build-essential \
        cmake \
        pkg-config \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libv4l-dev \
        libxvidcore-dev \
        libx264-dev \
        libgtk2.0-dev \
        libatlas-base-dev \
        gfortran \
        python3-dev && \
    apt-get clean

RUN pip3 install paho-mqtt==1.6.1
<<<<<<< HEAD
RUN pip3 install pycryptodome==3.21.0
=======
RUN pip3 install --no-cache-dir flask opencv-python-headless
>>>>>>> docker

COPY ./src /app/src

WORKDIR /app/src

EXPOSE 12345
EXPOSE 12346

CMD mosquitto -d && python3 /app/src/scripts/run.py