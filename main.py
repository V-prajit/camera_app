import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk
from threading import Thread

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")
        self.label = ttk.Label(root)
        self.label.pack(padx=10, pady=10)
        self.is_recording = False

        self.start_button = ttk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(padx=10, pady=10)
        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(padx=10, pady=10)
        self.process = None

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            command = [
                "ffmpeg",
                "-f", "avfoundation",
                "-i", "0",
                "-pix_fmt", "yuv420p",
                "-f", "rawvideo",
                "-"
            ]
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.update_gui()

    def stop_recording(self):
        self.is_recording = False
        if self.process:
            self.process.terminate()

    def update_gui(self):
        if self.is_recording:
            raw_frame = self.process.stdout.read(640 * 480 * 3)
            if raw_frame:
                img = self.convert_raw_frame_to_image(raw_frame)
                self.label.config(image=img)
                self.label.image = img
                self.root.after(10, self.update_gui)  # Update the GUI every 10 milliseconds
            else:
                self.process = None
                self.label.config(image="")
        else:
            self.label.config(image="")

    def convert_raw_frame_to_image(self, raw_frame):
        img = Image.frombytes('RGB', (640, 480), raw_frame)
        return ImageTk.PhotoImage(img)

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
