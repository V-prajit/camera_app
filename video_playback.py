#importing the required libraries
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
from tkinter import filedialog

#Setting Up The Tkinter Instance
app = Tk()
app.bind('<Escape>', lambda e: app.quit())

# Global variables and states
current_frame_num = 0
total_frames = 0
cap = None
vid_frame = None
is_paused = False
last_mouse_x = 0
last_mouse_y = 0
framerate = 30

# Labels for the Tkinter App
video_source = Label(app)
video_source.pack(pady=10)

controls_frame = Frame(app)
controls_frame.pack(pady=10)

frame_counter_label = Label(app, text="Frame: 0")
rgb_label = Label(app)

def show_frame(frame):
    global current_frame_num, total_frames, vid_frame
    current_frame_num += 1
    frame_counter_label.config(text=f"Frame: {current_frame_num}/{total_frames}")
    
    convert_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(convert_color)
    imgtk = ImageTk.PhotoImage(image=current_image)
    video_source.config(image=imgtk)
    video_source.imgtk = imgtk
    vid_frame = frame
    update_rgb_values()

def on_mouse_move(e):
    global last_mouse_x, last_mouse_y
    last_mouse_x, last_mouse_y = e.x, e.y
    update_rgb_values()

video_source.bind('<Motion>', on_mouse_move)

def update_rgb_values():
    global vid_frame, last_mouse_x, last_mouse_y, video_source
    if vid_frame is not None:
        label_w = video_source.winfo_width()
        label_h = video_source.winfo_height()
        frame_w = vid_frame.shape[1]
        frame_h = vid_frame.shape[0]
        x_scale = frame_w / label_w
        y_scale = frame_h / label_h
        x = int(last_mouse_x * x_scale)
        y = int(last_mouse_y * y_scale)
        if 0 <= x < frame_w and 0 <= y < frame_h:
            b, g, r = vid_frame[y, x]
            rgb = (r, g, b)
            rgb_label.config(text="RGB: {}".format(rgb))
        else:
            rgb_label.config(text="RGB: Out of bounds")

def move_frame_forward():
    global vid_frame, current_frame_num, cap
    if cap is not None and is_paused:
        ret, vid_frame = cap.read()
        if not ret:
            return
        show_frame(vid_frame)

def move_frame_backward():
    global vid_frame, current_frame_num, cap
    frame_that_is_playing = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    if cap is not None and is_paused:
        if frame_that_is_playing > 0:
            frame_that_is_playing -= 2
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_that_is_playing) 
            ret, vid_frame = cap.read()  
            if ret:
                current_frame_num -= 2
                show_frame(vid_frame)
            else:
                print("Error reading frame")
        else:
            print("Reached the beginning of the video")

def play_video():
    global cap, total_frames
    video_path = filedialog.askopenfilename(title="Select Video File", 
                                            filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")])

    if not video_path:
        print("No file selected!")
        return

    if not os.path.exists(video_path):
        print("Error: File doesn't exist!")
        return
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 

    rgb_label.pack()
    frame_counter_label.pack()
    rgb_label.pack()

    # Pack the video control buttons here
    pause_button.pack(side=LEFT, padx=5)
    move_forward_button.pack(side=LEFT, padx=5)
    move_backward_button.pack(side=LEFT, padx=5)

    controls_frame.pack(pady=10) 
    play_frame()

def play_frame():
    global cap, vid_frame
    if cap is not None and not is_paused:
        ret, vid_frame = cap.read()
        if ret:
            show_frame(vid_frame)
            app.after(1000 // framerate, play_frame)
        else:
            cap.release()

def pause_playback():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Resume Playback")
    else:
        pause_button.config(text="Pause Playback")
        play_frame()

#Buttons
play_button = Button(controls_frame, text='Play Video', command=play_video)
play_button.pack(side=LEFT, padx=5)

pause_button = Button(controls_frame, text='Pause Playback', command=pause_playback)
move_forward_button = Button(controls_frame, text='Move Frame Forward', command=move_frame_forward)
move_backward_button = Button(controls_frame, text='Move Frame Backward', command=move_frame_backward)

app.mainloop()
