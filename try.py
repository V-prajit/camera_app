from tkinter import *
import cv2
from PIL import Image, ImageTk

app = Tk()
app.bind('<Escape>', lambda e: app.quit())

# Global variables and states
cam = cv2.VideoCapture(0)
cam_width = int(cam.get(3))
cam_height = int(cam.get(4))
framerate = 60
write_video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), framerate, (cam_width, cam_height))

cur_frame = 0
recording_state = False
state_of_playback = False
is_paused = False
cap = None
live_preview = True
vid_frame = None
frame_cache = []

video_source = Label(app)
video_source.pack()
rgb_label = Label(app, text="RGB: ")
rgb_label.pack()

def show_frame(frame):
    convert_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(convert_color)
    imgtk = ImageTk.PhotoImage(image=current_image)
    video_source.config(image=imgtk)
    video_source.imgtk = imgtk

def preview_window():
    global live_preview
    _, frame = cam.read()
    show_frame(frame)

    if recording_state and not state_of_playback:
        write_video.write(frame)

    app.after(1000 // framerate, preview_window)

def play_frame():
    global cap, vid_frame, frame_cache
    if cap is not None and not is_paused:
        ret, vid_frame = cap.read()
        if ret:
            frame_cache.append(vid_frame)
            show_frame(vid_frame)
            app.after(1000 // framerate, play_frame)
        else:
            cap.release()
            recording_button.config(text="Start Recording")

def pause_playback():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        pause_button.config(text="Resume Playback")
    else:
        pause_button.config(text="Pause Playback")
        play_frame()

def play_video():
    global cap, recording_state, live_preview, frame_cache
    if cam.isOpened():
        cam.release()

    cap = cv2.VideoCapture('output.avi')
    recording_state = False
    live_preview = False
    frame_cache = []
    recording_button.config(text="Start Recording")
    play_frame()

def get_rgb_values(event):
    global vid_frame, live_preview
    x, y = event.x, event.y
    if not live_preview and vid_frame is not None:
        if x < vid_frame.shape[1] and y < vid_frame.shape[0]:
            rgb = vid_frame[y, x]
            rgb_label.config(text="RGB: {}".format(rgb))
        else:
            rgb_label.config(text="RGB: Out of bounds")

def toggle_recording():
    global recording_state
    recording_state = not recording_state
    if recording_state:
        recording_button.config(text="Stop Recording")
    else:
        recording_button.config(text="Start Recording")

def move_frame_forward():
    global cap, vid_frame, frame_cache
    if cap is not None and is_paused:
        ret, vid_frame = cap.read()
        if ret:
            frame_cache.append(vid_frame)
            show_frame(vid_frame)
        else:
            print("Reached the end of the video")

def move_frame_backward():
    global vid_frame, frame_cache
    if frame_cache:
        vid_frame = frame_cache.pop()
        show_frame(vid_frame)
    else:
        print("Reached the beginning of the video")

# Call the preview_window function to start displaying the video
preview_window()

# Bind the mouse motion event to get_rgb_values function:
video_source.bind('<Motion>', get_rgb_values)

# UI Buttons
recording_button = Button(app, text='Start Recording', command=toggle_recording)
recording_button.pack()

pause_button = Button(app, text='Pause Playback', command=pause_playback)
pause_button.pack()

play_button = Button(app, text='Play Video', command=play_video)
play_button.pack()

move_forward_button = Button(app, text='Move Frame Forward', command=move_frame_forward)
move_forward_button.pack()

move_backward_button = Button(app, text='Move Frame Backward', command=move_frame_backward)
move_backward_button.pack()

app.mainloop()
