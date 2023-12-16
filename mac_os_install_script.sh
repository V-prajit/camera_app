#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3.9 &> /dev/null; then
    echo "Python 3.9 is not installed. Installing Python 3..."

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Installing Homebrew..."
        
        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        if [ $? -ne 0 ]; then
            echo "Failed to install Homebrew."
            exit 1
        fi

        # Configure the shell to include Homebrew in PATH
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    # Install Python 3 using Homebrew
    echo "Installing Python 3 using Homebrew..."
    brew install python@3.9
    if [ $? -ne 0 ]; then
        echo "Failed to install Python 3."
        exit 1
    fi

    echo "Python 3 has been successfully installed."
else 
    echo "Python 3 is already installed."
fi

# Check and install Tkinter if necessary
python3.9 -m tkinter --version &> /dev/null
if [ $? -ne 0 ]; then
    echo "Tkinter is not installed. Installing Tkinter..."
    brew install python-tk@3.9
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

echo "Try recording your first video by running "python3.9 record_video.py""