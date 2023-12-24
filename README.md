# A Camera App

## Key Parts
- **Record a Video:** Enables recording with real-time camera view and a custom filename.
- **Open a Video:** Allows checking the specific RGB values of a single pixel in a video.
- **Control Video Playback:** Move the video playback forward or backward by a single frame.
- **Motion Tracking:** Track the maximum and minimum angles to determine the range of motion of an arm in a recorded video.

## How To Use
<div style="text-align:center">
    <a href="#windows">Windows</a> &middot; <a href="#macos">macOS</a> &middot; <a href="#ubuntu">Ubuntu</a>
</div>

### Windows
(Instructions for Windows users will be added here.)

### macOS
To download all files and install Python, choose one of the following methods:

#### Install Script
1. Open the macOS terminal and copy-paste the following code: 
    ```bash
    bash <(curl -sL https://raw.githubusercontent.com/V-prajit/camera_app/install_scripts/mac_os_install_script.sh)
    ```
2. Enter your macOS password into the terminal when prompted.
3. Press the Enter key when prompted.
4. To run your first app, open the terminal in the downloaded folder and execute:
    ```bash
    python3 record_video.py 
    ```

#### Manual Installation
1. Download the GitHub repository as shown in the tutorial video below.
2. Install Python from [this website](website link) (See Tutorial Video).
3. Install all the dependencies by copy-pasting this code into the terminal:
    ```bash
    pip3 install opencv-python mediapipe Pillow numpy
    ```
4. To run your first app, open the terminal in the downloaded folder and execute:
    ```bash
    python3 record_video.py

### Ubuntu
(Instructions for Ubuntu users will be added here.)
