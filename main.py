from tkinter import *
import cv2
from PIL import Image, ImageTk

#set the camera and its values up
cam = cv2.VideoCapture(0)
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
framerate = int(cam.get(5))

#setting the base window
app = Tk()
app.bind('<Escape>', lambda e: app.quit())

#place the video feed into tkinter video
vid_src = Label(app)
vid_src.pack()

global recording_state
recording_state = False
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), framerate, (frame_width,frame_height))

#functions to perform actions
#open the camera preview upon opeing the application
def open_camera():
    _, frame = cam.read()
    c_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cur_frame = Image.fromarray(c_image)
    photo_cur_frame = ImageTk.PhotoImage(image = cur_frame)
    vid_src.photo_image = photo_cur_frame
    vid_src.configure(image = photo_cur_frame)
    vid_src.after(10, open_camera)

#state of the recording button, and having it start and stop writing to a file
def state1():
    global recording_state
    recording_state = True
    rec_button.configure(text = "Stop Recording", command = state2)
def state2():
    global recording_state
    recording_state = False
    rec_button.configure(text = "Start Recording", command = state1)
if recording_state == True:
    out.write(cam.read())
out.release()
rec_button = Button(app, text = 'Start Recording', command = state2)
rec_button.pack()
app.after(1, open_camera)

app.mainloop()



