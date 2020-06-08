FROM ubuntu:18.04

# avoiding user interatition
ARG DEBIAN_FRONTEND=noninteractive

# install necessaries packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3 python3-dev \
    wget ca-certificates \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \ 
    libgtk2.0-dev libatlas-base-dev gfortran \
    libjpeg-dev libtiff-dev libpng-dev \
    ffmpeg x264 libx264-dev

# installing opencv using apt-get
RUN apt-get install --no-install-recommends -y python3-opencv

# getting pip3
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm -f get-pip.py

# copying project
WORKDIR /opt/is
COPY src/ src
COPY etc/conf etc/conf
COPY setup.py ./setup.py
RUN pip3 install .



ENTRYPOINT ["mock-cameras"]