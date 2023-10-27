from tkinter import *
import cv2 
from PIL import Image, ImageTk

# start the tkinter window.
app = Tk()
app.bind('<Escape>', lambda e: app.quit()) # bind the escape key to quiting the app.

# defining the global values
cam = cv2.VideoCapture(0)
cam_width = int(cam.get(3))
cam_height = int(cam.get(4))
framerate = 30
frame_counter = 0
write_video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('M','J','P','G'), framerate, (cam_width, cam_height))
# defining states for loops and change in functions
state_of_video = "Preview"
cur_frame = 0
recording_state = False
state_of_playback = False

# Label for the Tkinter app 
video_source = Label(app)
video_source.pack()

# Global variable to hold the PhotoImage object
display_in_Tkinter = None
preview_window_id = None

def preview_window():
    global display_in_Tkinter, preview_window_id
    
    _, frame = cam.read()

    convert_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
    current_image = Image.fromarray(convert_color)
    display_in_Tkinter = ImageTk.PhotoImage(image=current_image)
    video_source.configure(image=display_in_Tkinter)
    video_source.image = display_in_Tkinter  # Keep a reference to prevent garbage collection
    
    if recording_state and not state_of_playback:
        write_video.write(frame)

    # Call the function again after 1 millisecond
    preview_window_id = app.after(1000 // framerate, preview_window)

def play_video():
    global frame_counter, cam, preview_window_id

    if cam.isOpened():
        cam.release()
    if preview_window_id:
        app.after_cancel(preview_window_id)

    cap = cv2.VideoCapture('output.avi')

    def play_frame():
        nonlocal cap
        ret, vid_frame = cap.read()
        if ret:
            convert_color_p = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGBA) 
            current_image_p = Image.fromarray(convert_color_p)
            display_in_Tkinter_p = ImageTk.PhotoImage(image=current_image_p)
            video_source.configure(image=display_in_Tkinter_p)
            video_source.image = display_in_Tkinter_p  # Keep a reference to prevent garbage collection
            # Schedule the next frame
            video_source.after(1000 // framerate, play_frame)
        else:
            # When the video ends, release the capture object and reset UI
            cap.release()
            recording_button.configure(text="Start Recording")

    # Start playing frames
    play_frame()

# Rest of your code...



def toggle_recording():
    global recording_state
    recording_state = not recording_state
    if recording_state:
        recording_button.configure(text = "Stop Recording")
    else:
        recording_button.configure(text = "Start Recording")

# Call the preview_window function to start displaying the video
preview_window()

recording_button = Button(app, text='Start Recording', command=toggle_recording)
recording_button.pack()

play_button = Button(app, text = 'play Video', command = play_video)
play_button.pack()
# Start the Tkinter main loop
app.mainloop()
