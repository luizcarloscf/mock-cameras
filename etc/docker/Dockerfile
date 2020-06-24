FROM ubuntu:18.04

# avoiding user interatition
ARG DEBIAN_FRONTEND=noninteractive

# install necessaries packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3.6 python3.6-dev \
    wget ca-certificates build-essential cmake pkg-config unzip\
    libsm6 libxext6 libxrender-dev libglib2.0-0 \
    libjpeg-dev libpng-dev libtiff-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libatlas-base-dev gfortran \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \
    x264 libx264-dev

# getting pip3
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm -f get-pip.py

RUN pip3 install numpy

WORKDIR /tmp/
RUN wget -O opencv.tar.gz https://github.com/opencv/opencv/archive/4.3.0.tar.gz && \
    tar xf opencv.tar.gz  && \
    rm -rf opencv.tar.gz

WORKDIR /tmp/opencv-4.3.0/build
RUN cmake \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D WITH_QT=OFF \
        -D WITH_GTK=OFF \
        -D WITH_CUDA=OFF \
        -D WITH_FFMPEG=ON \
        -D BUILD_FFMPEG=ON \
        -D BUILD_opencv_java=OFF \
        -D CMAKE_INSTALL_PREFIX=/usr/local\
        -D BUILD_opencv_python3=ON \
        -D BUILD_DOCS=NO \
        -D BUILD_PERF_TESTS=OFF \
        -D BUILD_TESTS=OFF \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_opencv_python2=NO \
        -D PYTHON3_EXECUTABLE=/usr/bin/python3 \
        -D PYTHON3_INCLUDE_DIR=$(/usr/bin/python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
        -D PYTHON3_PACKAGES_PATH=$(/usr/bin/python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") .. \
        .. \
    && make -j2 \
    && make install \
    && cd ../../ && rm -rf opencv-4.3.0

# installing packages on requiments.txt with pip3
WORKDIR /opt/is

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm -f requirements.txt
COPY src/ src
COPY etc/conf etc/conf

ENTRYPOINT ["python3", "src/service.py"]