from tkinter import *
import cv2
from PIL import Image, ImageTk

# set the camera and its values up
cam = cv2.VideoCapture(0)
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
framerate = int(cam.get(5))

# setting the base window
app = Tk()
app.bind('<Escape>', lambda e: app.quit())

# place the video feed into tkinter video
vid_src = Label(app)
vid_src.pack()

global recording_state
recording_state = False
out = None

# functions to perform actions
# open the camera preview upon opening the application
def open_camera():
    global recording_state, out
    _, frame = cam.read()
    c_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cur_frame = Image.fromarray(c_image)
    photo_cur_frame = ImageTk.PhotoImage(image=cur_frame)
    vid_src.photo_image = photo_cur_frame
    vid_src.configure(image=photo_cur_frame)

    if recording_state:
        if out is None:
            out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), framerate, (frame_width, frame_height))
        out.write(frame)
    vid_src.after(10, open_camera)

def play_video():
    cap = cv2.VideoCapture('outpy.avi')

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Recorded Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

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

play_button = Button(app, text='Play Recorded Video', command=play_video)
play_button.pack()

app.after(1, open_camera)
app.mainloop()
