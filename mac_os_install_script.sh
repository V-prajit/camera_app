#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing Python 3..."

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Installing Homebrew..."
        
        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        if [ $? -ne 0 ]; then
            echo "Failed to install Homebrew."
            exit 1
        fi
    fi

    # Install Python 3 using Homebrew
    echo "Installing Python 3 using Homebrew..."
    brew install python3
    if [ $? -ne 0 ]; then
        echo "Failed to install Python 3."
        exit 1
    fi

    echo "Python 3 has been successfully installed."
else 
    echo "Python 3 is already installed."
fi

