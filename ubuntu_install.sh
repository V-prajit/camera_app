#!/bin/bash

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11 is not installed. Installing Python 3.11..."

    # Update package list
    sudo apt-get update

    # Install Python 3.11
    sudo apt-get install -y python3.11
    if [ $? -ne 0 ]; then
        echo "Failed to install Python 3.11."
        exit 1
    fi

    echo "Python 3.11 has been successfully installed."
else
    echo "Python 3.11 is already installed."
fi

sudo apt-get update
sudo apt-get install -y python3-pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade Pillow."
    exit 1
fi

# Check and install Tkinter if necessary
python3.11 -m tkinter --version &> /dev/null
if [ $? -ne 0 ]; then
    echo "Tkinter is not installed. Installing Tkinter..."
    sudo apt-get install -y python-tk 
    if [ $? -ne 0 ]; then
        echo "Failed to install Tkinter."
        exit 1
    fi
else
    echo "Tkinter is already installed."
fi

# Install additional Python packages
echo "Installing additional Python packages..."
python3.11 -m pip install opencv-python mediapipe Pillow numpy
if [ $? -ne 0 ]; then
    echo "Failed to install one or more Python packages."
    exit 1
fi

echo "Upgrading Pillow..."
sudo python3.11 -m pip install Pillow --upgrade
if [ $? -ne 0 ]; then
    echo "Failed to upgrade Pillow."
    exit 1
fi

sudo apt install -y python3-tk
if [$? -ne 0 ]; then
	echo "Failed to install Tkinter"
	exit 1
fi


echo "All required Python packages have been successfully installed."

echo "Try recording your first video by running 'python3.11 record_video.py'"
