import tkinter as tk
from tkinter import ttk
import imageio
from PIL import Image, ImageTk
app = tk.Tk()
app.title("The Camera App")

#Get frames from the webcam
def get_frame():
    input = imageio.get_reader("<video0", format="ffmpeg", mode = "I", input_params=["-r", "30"])

    for frame in input:
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img

        if root.winfo.exists() == 0:
            break

get_frame()
#Button to toogle screen recordign
def Toggle_screen_recording():
    label.config(text = "button Clicked!")

button = tk.Button(app, text = "Click Me!", command = Toggle_screen_recording)
button.pack()




app.mainloop()