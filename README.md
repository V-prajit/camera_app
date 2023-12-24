# A Camera App

## Key Parts
- **Record a Video:** Enables recording with a real-time camera view and a custom filename.
- **Open a Video:** Allows checking the specific RGB values of a single pixel in a video.
- **Control Video Playback:** Move the video playback forward or backward by a single frame.
- **Motion Tracking:** Track the maximum and minimum angles to determine the range of motion of an arm in a recorded video.

## How To Install
<div style="text-align:center">
    <strong><a href="#windows">Windows</a> &middot; <a href="#macos">MacOS</a> &middot; <a href="#ubuntu">Ubuntu</a></strong>
</div>

### Windows
To download all files and install Python, choose one of the following methods:
#### Install Script
1. Open Windows PowerShell and copy-paste the following code: 
    ```bash
    Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/V-prajit/camera_app/install_scripts/windows_install_script.ps1" -UseBasicParsing).Content
    ```
2. Enter your Windows login password into the terminal when prompted.
3. Press the Enter key when prompted.
4. To run your first app, open PowerShell in the downloaded folder and execute:
    ```bash
    python record_video.py 
    ```

#### Manual Installation
1. Download the GitHub repository as shown in the tutorial video below.
2. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) 
[See Tutorial Video](https://www.youtube.com/watch?v=P7Q4_pqj7uc&ab_channel=AmitThinks).
3. Install all the dependencies by copy-pasting this code into PowerShell:
    ```bash
    pip install opencv-python mediapipe Pillow numpy
    ```
4. To run your first app, open PowerShell in the downloaded folder and execute:
    ```bash
    python record_video.py
    ```

### MacOS
To download all files and install Python, choose one of the following methods:

#### Install Script
1. Open the macOS terminal and copy-paste the following code: 
    ```bash
    bash <(curl -sL https://raw.githubusercontent.com/V-prajit/camera_app/install_scripts/mac_os_install_script.sh)
    ```
2. Enter your macOS login password into the terminal when prompted.
3. Press the Enter key when prompted.
4. To run your first app, open the terminal in the downloaded folder and execute:
    ```bash
    python3 record_video.py 
    ```

#### Manual Installation
1. Download the GitHub repository as shown in the tutorial video below.
2. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) 
[See Tutorial Video](https://www.youtube.com/watch?v=oKIjWmoLXOo&ab_channel=MacintoshWeekly).
3. Install all the dependencies by copy-pasting this code into the terminal:
    ```bash
    pip3 install opencv-python mediapipe Pillow numpy
    ```
4. To run your first app, open the terminal in the downloaded folder and execute:
    ```bash
    python3 record_video.py
    ```

### Ubuntu
To download all files and install Python, choose one of the following methods:
#### Install Script
1. Open the Ubuntu terminal and copy-paste the following code: 
    ```bash
    wget -O - https://raw.githubusercontent.com/V-prajit/camera_app/install_scripts/ubuntu_install.sh | sudo bash
    ```
2. Enter your Ubuntu login password into the terminal when prompted.
3. Press the Enter key when prompted.
4. To run your first app, open the terminal in the downloaded folder and execute:
    ```bash
    python3 record_video.py 
    ```

#### Manual Installation
1. Download the GitHub repository as shown in the tutorial video below.
2. Install Python by running these lines in the terminal:
    ```bash
    sudo apt-get install python3 && sudo apt-get install python3-pip
    ```
    [See Tutorial Video](https://www.youtube.com/watch?v=IAco2SSuGms&ab_channel=AmitThinks).
3. Install all the dependencies by copy-pasting this code into the terminal:
    ```bash
    pip3 install opencv-python mediapipe Pillow numpy
    ```
4. To run your first app, open the terminal in the downloaded folder and execute:
    ```bash
    python3 record_video.py
    ```
