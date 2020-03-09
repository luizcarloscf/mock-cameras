#!/bin/bash
	
# Get super user privileges
if [[ $EUID != 0 ]]; then
  export wasnt_root=true
  sudo -E "$0" "$@"
fi

if [[ $EUID == 0 ]]; then

  apt-get purge -y python-opencv python3-opencv

  packages=(python3 python3-dev \
    ca-certificates \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \ 
    libgtk2.0-dev libatlas-base-dev gfortran \
    libjpeg-dev libtiff-dev libpng-dev \
    ffmpeg x264 libx264-dev)
    echo "[$EUID] |>>| installing distro packages: ${packages[*]}"
    apt-get update
    apt-get install --no-install-recommends -y ${packages[*]} 

  if ! command -v pip3 > /dev/null; then 
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    rm -f get-pip.py
  fi
fi

if [[ $EUID != 0 || -z ${wasnt_root} ]]; then
  pip3 uninstall --yes opencv-python
  pip3 install -r requirements.txt
  apt-get install --no-install-recommends -y python3-opencv
fi