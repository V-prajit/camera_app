from tkinter import *
import cv2
from PIL import Image, ImageTk

app = Tk()
app.bind('<Escape>', lambda e: app.quit())

# Global variables and states
cam = cv2.VideoCapture(0)
cam_width = int(cam.get(3))
cam_height = int(cam.get(4))
framerate = 30
write_video = None
recording_state = False

video_source = Label(app)
video_source.pack(pady = 10)
controls_frame = Frame(app)
controls_frame.pack(pady=10)

filename_label = Label(controls_frame, text="Filename:")
filename_label.pack(side=LEFT, padx=5)
filename_entry = Entry(controls_frame, width=20)
filename_entry.pack(side=LEFT, padx=5)
filename_entry.insert(0, "output.mp4")

def show_frame(frame):
    global vid_frame
    convert_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(convert_color)
    imgtk = ImageTk.PhotoImage(image=current_image)
    video_source.config(image=imgtk)
    video_source.imgtk = imgtk


def preview_window():
    global live_preview
    _, frame = cam.read()
    show_frame(frame)

    if recording_state:
        write_video.write(frame)
    app.after(1000 // framerate, preview_window)

def toggle_recording():
    global recording_state, write_video
    recording_state = not recording_state
    if recording_state:
        recording_button.config(text="Stop Recording")
        filename = filename_entry.get()
        if not filename.endswith('.mp4'):
            filename += '.mp4'
        write_video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), framerate, (cam_width, cam_height))
    else:
        recording_button.config(text="Start Recording")
        if write_video:
            write_video.release()

# Buttons
recording_button = Button(controls_frame, text='Start Recording', command=toggle_recording)
recording_button.pack(side=LEFT, padx=5)

# Start the preview
preview_window()

app.mainloop()

