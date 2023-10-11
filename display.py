import tkinter as tk
from tkinter import ttk
import imageio
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Video Player")

frame_number_label = ttk.label(root, text="Frame:0")
frame_number_label.pack()

video_path = "C:\Users\shash\OneDrive\Desktop\Camera app/video.mp4"
video_reader = imageio.get_reader(video_path)

def update_frame_lable(frame_number):
    frame_number_label.config(text=f"Frame: {frame_number}")

def u