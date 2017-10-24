from Tkinter import *
# import ttk
from PIL import ImageTk, Image
# import os
import Tkinter as tk
#import ImageTk

################################################################################







################################################################################

root = tk.Tk()

imgFrame = Frame(width=600, height=600)
imgFrame.pack()

img = ImageTk.PhotoImage(Image.open('bolbi.jpg'))
panel = tk.Label(imgFrame, image=img)
panel.pack(side="top", fill="both", expand="yes")

### load frame
loadFrame = Frame(width=600)
loadFrame.pack()

ent = Entry(loadFrame)
ent.pack(side=LEFT)

def callback():
    file_name = ent.get()
    print 'trying to load: ' + str(file_name)
    img2 = ImageTk.PhotoImage(Image.open(file_name))
    panel.configure(image=img2)
    panel.image = img2

def drawer():
    print 'drawing'

btnEnter = Button(loadFrame, text='Load file', command=callback)
btnEnter.pack(side=LEFT)

lineFrame = Frame(width=600)
lineFrame.pack()

x1 = Entry(lineFrame, text='x1')
x1.pack(side=LEFT)
y1 = Entry(lineFrame, text='y1')
y1.pack(side=LEFT)
x2 = Entry(lineFrame, text='x2')
x2.pack(side=LEFT)
y2 = Entry(lineFrame, text='y2')
y2.pack(side=LEFT)

btnDraw = Button(lineFrame, text='Draw', command=drawer)
btnDraw.pack(side=LEFT)

root.bind("d", drawer)
root.bind("<Return>", callback)
root.mainloop()
