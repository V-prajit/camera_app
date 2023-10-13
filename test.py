from tkinter import *

app = Tk()
app.bind('<Escape>', lambda e: app.quit())
app.minsize(1280, 720)

text = Label(app)
text.pack()

rec_button = Button(app, text = 'Start Recording')
rec_button.pack()


app.mainloop()