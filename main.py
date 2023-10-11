import tkinter as tk

app = tk.Tk()
app.title("The Camera App")

label = tk.Label(app, text = "hello World")
label.pack()

def Toggle_screen_recording():
    label.config(text = "button Clicked!")

button = tk.Button(app, text = "Click Me!", command = Toggle_screen_recording)
button.pack()

app.mainloop()