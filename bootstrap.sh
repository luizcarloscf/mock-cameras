#!/bin/bash
	
# Get super user privileges
if [[ $EUID != 0 ]]; then
  export wasnt_root=true
  sudo -E "$0" "$@"
fi

if [[ $EUID == 0 ]]; then

  #removing OpenCV
  apt-get purge -y python-opencv python3-opencv

  #installing packages for OpenCV
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

  #getting pip3
  if ! command -v pip3 > /dev/null; then 
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    rm -f get-pip.py
  fi
  #installing openCV
  apt-get install --no-install-recommends -y python3-opencv
fi

if [[ $EUID != 0 || -z ${wasnt_root} ]]; then
  #remove opencv installed by pip3
  pip3 uninstall --yes opencv-python

  #installing packages listed at requirements.txt
  pip3 install -r requirements.txt
  
fi