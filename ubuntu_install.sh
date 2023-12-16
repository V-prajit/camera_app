#!/bin/bash

# Check if Python 3.9 is installed
if ! command -v python3.9 &> /dev/null; then
    echo "Python 3.9 is not installed. Installing Python 3.9..."

    # Update package list
    sudo apt-get update

    # Install Python 3.9
    sudo apt-get install -y python3.9
    if [ $? -ne 0 ]; then
        echo "Failed to install Python 3.9."
        exit 1
    fi

    echo "Python 3.9 has been successfully installed."
else
    echo "Python 3.9 is already installed."
fi

# Check and install Tkinter if necessary
python3.9 -m tkinter --version &> /dev/null
if [ $? -ne 0 ]; then
    echo "Tkinter is not installed. Installing Tkinter..."
    sudo apt-get install -y python3.9-tk
    if [ $? -ne 0 ]; then
        echo "Failed to install Tkinter."
        exit 1
    fi
else
    echo "Tkinter is already installed."
fi

# Install additional Python packages
echo "Installing additional Python packages..."
pip3.9 install opencv-python mediapipe Pillow numpy
if [ $? -ne 0 ]; then
    echo "Failed to install one or more Python packages."
    exit 1
fi

echo "All required Python packages have been successfully installed."

echo "Try recording your first video by running 'python3.9 record_video.py'"

