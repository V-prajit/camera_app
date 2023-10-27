from tkinter import *
import cv2
from PIL import Image, ImageTk
import threading

# set the camera and its values up
cam = cv2.VideoCapture(0)
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
framerate = 60  # Set the frame rate for recording and playback (in frames per second)

# Initialize video writer
out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), framerate, (frame_width, frame_height))

# setting the base window
app = Tk()
app.bind('<Escape>', lambda e: app.quit())

# place the video feed into tkinter video
vid_src = Label(app)
vid_src.pack()

frame_count_label = Label(app, text="Frame: 0")
frame_count_label.pack()

rgb_label = Label(app, text="RGB: ")
rgb_label.pack()

global recording_state, paused, next_or_prev_frame
recording_state = False
paused = False
next_or_prev_frame = None

total_frames = 0  # Variable to keep track of the total frames recorded

# functions to perform actions
# open the camera preview upon opening the application
def open_camera():
    global recording_state, paused, total_frames
    _, frame = cam.read()
    frame = cv2.resize(frame, (frame_width, frame_height))

    c_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cur_frame = Image.fromarray(c_image)
    photo_cur_frame = ImageTk.PhotoImage(image=cur_frame)
    vid_src.photo_image = photo_cur_frame
    vid_src.configure(image=photo_cur_frame)

    vid_src.bind("<Motion>", get_rgb_values)

    if recording_state and not paused:
        out.write(frame)  # Write frame to video file
        total_frames += 1  # Increase the total frames recorded
    vid_src.after(1000 // framerate, open_camera)  # Use the specified frame rate for capturing frames

def get_rgb_values(event):
    x, y = event.x, event.y  # Get the coordinates of the mouse cursor
    frame = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2RGB)  # Read the current frame
    rgb = frame[y, x]  # Get the RGB values at the cursor position
    rgb_label.config(text="RGB: {}".format(rgb))

def play_video():
    global paused, next_or_prev_frame, total_frames
    global current_frame
    current_frame = 0

    cap = cv2.VideoCapture('outpy.avi')

    while True:
        if not paused or (paused and next_or_prev_frame is not None):
            if next_or_prev_frame == "next":
                current_frame += 1
            elif next_or_prev_frame == "prev":
                current_frame -= 1

            # Ensure the current_frame stays within the valid range
            current_frame = max(0, min(total_frames - 1, current_frame))

            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()

            if not ret:
                break

            frame_count_label.config(text="Frame: {}".format(current_frame))

            next_or_prev_frame = None

        cv2.imshow('Recorded Video', frame)

        if cv2.waitKey(1000 // framerate) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ... (rest of your code remains the same)

def pause_resume_video():
    global paused
    paused = not paused

def next_frame():
    global next_or_prev_frame
    next_or_prev_frame = "next"

def prev_frame():
    global next_or_prev_frame
    next_or_prev_frame = "prev"

# state of the recording button, and having it start and stop writing to a file
def toggle_recording():
    global recording_state
    recording_state = not recording_state
    if recording_state:
        rec_button.configure(text="Stop Recording")
    else:
        rec_button.configure(text="Start Recording")

rec_button = Button(app, text='Start Recording', command=toggle_recording)
rec_button.pack()

play_button = Button(app, text='Play Recorded Video', command=lambda: threading.Thread(target=play_video).start())
play_button.pack()

pause_resume_button = Button(app, text='Pause/Resume Video', command=pause_resume_video)
pause_resume_button.pack()

forward_button = Button(app, text='Move Forward', command=next_frame)
forward_button.pack()

backward_button = Button(app, text='Move Backward', command=prev_frame)
backward_button.pack()

# random comment
app.after(1, open_camera)
app.mainloop()
