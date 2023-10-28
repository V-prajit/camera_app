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

recording_state = False
is_paused = False
cap = None
live_preview = True
vid_frame = None
frame_cache = []

video_source = Label(app)
video_source.pack(pady=10)

controls_frame = Frame(app)
controls_frame.pack(pady=10)

rgb_label = Label(app)

def show_frame(frame):
    convert_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    current_image = Image.fromarray(convert_color)
    imgtk = ImageTk.PhotoImage(image=current_image)
    video_source.config(image=imgtk)
    video_source.imgtk = imgtk

def update_rgb_values(x, y):
    if vid_frame is not None:
        if 0 <= x < vid_frame.shape[1] and 0 <= y < vid_frame.shape[0]:
            rgb = vid_frame[y, x]
            rgb_label.config(text="RGB: {}".format(rgb))
        else:
            rgb_label.config(text="RGB: Out of bounds")

def move_frame_forward():
    global vid_frame, frame_cache
    if cap is not None and is_paused:
        ret, vid_frame = cap.read()
        if ret:
            frame_cache.append(vid_frame)
            show_frame(vid_frame)
        else:
            reset_to_start()

def move_frame_backward():
    global vid_frame, frame_cache
    if frame_cache:
        vid_frame = frame_cache.pop(-2)  # get the previous frame
        show_frame(vid_frame)
        if cap is not None:
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 2)
    else:
        print("Reached the beginning of the video")

def reset_to_start():
    global recording_state, is_paused, live_preview, vid_frame, frame_cache, cap
    recording_state = False
    is_paused = False
    live_preview = True
    vid_frame = None
    frame_cache = []
    rgb_label.pack_forget()
    controls_frame.pack_forget()
    recording_button.pack(side=LEFT, padx=5)
    play_button.pack(side=LEFT, padx=5)
    if cap is not None:
        cap.release()
        cap = None

# Rest of the functions
def preview_window():
    global live_preview
    _, frame = cam.read()
    show_frame(frame)

    if recording_state and not is_paused:
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

    recording_button.pack_forget()
    play_button.pack_forget()
    rgb_label.pack()
    
    # Pack the video control buttons here
    pause_button.pack(side=LEFT, padx=5)
    move_forward_button.pack(side=LEFT, padx=5)
    move_backward_button.pack(side=LEFT, padx=5)

    controls_frame.pack(pady=10)  # Ensure controls frame is packed after its content
    play_frame()


def toggle_recording():
    global recording_state
    recording_state = not recording_state
    if recording_state:
        recording_button.config(text="Stop Recording")
    else:
        recording_button.config(text="Start Recording")

video_source.bind('<Motion>', lambda e: update_rgb_values(e.x, e.y))

# UI Buttons
recording_button = Button(controls_frame, text='Start Recording', command=toggle_recording)
recording_button.pack(side=LEFT, padx=5)

play_button = Button(controls_frame, text='Play Video', command=play_video)
play_button.pack(side=LEFT, padx=5)

pause_button = Button(controls_frame, text='Pause Playback', command=pause_playback)
move_forward_button = Button(controls_frame, text='Move Frame Forward', command=move_frame_forward)
move_backward_button = Button(controls_frame, text='Move Frame Backward', command=move_frame_backward)

# Start the preview
preview_window()

app.mainloop()
