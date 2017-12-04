from Tkinter import *
from PIL import ImageTk, Image
import os
import Tkinter as tk
import shutil
import math

file_name = 'bolbi.jpg'
image = Image.open(file_name)
shutil.copy(file_name,file_name + '.temp.jpg')
image_temp = Image.open(file_name + '.temp.jpg')

global scan_lines_loaded
global scan_lines_current
decoded  = []
endoced  = []
decoded_str = ''

root = tk.Tk()

imgFrame = Frame(width=600, height=600)
imgFrame.pack()

img = ImageTk.PhotoImage(image)
panel = tk.Label(imgFrame, image=img)
panel.pack(side="top", fill="both", expand="yes")

### load frame
loadFrame = Frame(width=600)
loadFrame.pack()

ent = Entry(loadFrame)
ent.insert(END,'image file name')
ent.pack(side=LEFT)

def callback():
    file_name = ent.get()
    print 'trying to load: ' + str(file_name)

    image = Image.open(file_name)
    shutil.copy(file_name,file_name + '.temp.jpg')
    image_temp = Image.open(file_name + '.temp.jpg')

    img2 = ImageTk.PhotoImage(image_temp)
    panel.configure(image=img2)
    panel.image = img2

def saver():
    print 'saving edits to ' + file_name + ' as ' + file_name + '.temp.jpg'
    image_temp.save(file_name + '.temp.jpg')


btnEnter = Button(loadFrame, text='Load Image File', command=callback)
btnEnter.pack(side=LEFT)

btnSave = Button(loadFrame, text='Save Image File', command=saver)
btnSave.pack(side=LEFT)

######### Steg Frame

stegFrame = Frame(width=600)
stegFrame.pack()

text = Entry(stegFrame)
text.insert(END,'text to encode')
text.pack(side=LEFT)

def encode():
    print 'encoding ...'
    # read value for each pixel
    pixels = image_temp.load()
    to_encode = text.get()
    bin_encode = ''
    for x in to_encode:
        #e = str(bin(ord(x))).replace('0b','')
        #print ord(x)
        e = format(ord(x),'08b')
        # e = ''
        # e = str(bin(ord(x))).replace('0b','')
        # print e
        # if len(e) == 7:
        #     print '>> 7'
        # if len(e) == 6:
        #     print '>> 7'
        # # while (len(e) > 8):
        # #     e = '0' + e
        bin_encode = bin_encode + e
    #print bin_encode
    #print to_encode
    n = 0
    i = 0
    j = 0
    for char in bin_encode:
        # print '--'
        # print char
        # print 'before: ' + str(pixels[0,i])
        if (i == 500):
            j = j + 1
            i = 0

        print str(i) + ',' + str(j)

        if int(char)%2 == 0 and pixels[j,i][0]%2 == 1:
            pixels[j,i] = (pixels[j,i][0] + 1, pixels[j,i][1], pixels[j,i][2])
        elif int(char)%2 == 1 and pixels[j,i][0]%2 == 0:
            pixels[j,i] = (pixels[j,i][0] - 1, pixels[j,i][1], pixels[j,i][2])

        # print 'after: ' + str(pixels[0,i])
        # print '--'
        i = i + 1

    # for x in range(0,500):
    #     for y in range(0,500):
    #         if (n > len(bin_encode)):
    #             print 'oh'
    #             break
    #         else:
    #             if int(bin_encode[n])%2 and not pixels[x,y][0]%2:
    #                 pixels[x,y] = (pixels[x,y][0] + 1,pixels[x,y][1],pixels[x,y][2])
    #             else:
    #                 pixels[x,y] = (pixels[x,y][0] - 1,pixels[x,y][1],pixels[x,y][2])
    #             n = n + 1




    #pixels[0,0] = (255,0,0)
    wline = ImageTk.PhotoImage(image_temp)
    panel.configure(image=wline)
    panel.image = wline
    print 'done!'



def decode():
    print 'decoding ...'
    # read value for each pixel
    pixels = image_temp.load()
    for x in range(0,500):
        for y in range(0,500):
            #print str(x) + ',' + str(y) + ' = ' + str(pixels[x,y])
            r = (pixels[x,y][0])%2
            # print '--'
            # print pixels[x,y][0]
            # print r
            # print '--'
            #g = (pixels[x,y][1])%2
            #b = (pixels[x,y][2])%2
            decoded.append(r)
            #decoded.append(g)
            #decoded.append(b)
    #print decoded
    n = 1
    int_str = ''
    decoded_str = ''
    count = 0
    for x in range(0,len(decoded)-8,8):
        #print decoded[x:x+8]
        convert_str = ''
        for y in decoded[x:x+8]:
            convert_str = convert_str + str(y)
        char = chr(int(convert_str, 2))
        decoded_str = decoded_str + char
        # if count > 500:
        #     break
        count = count + 1

    print decoded_str + '\n'
    print 'done!'


btnEn = Button(stegFrame, text='Encode File', command=encode)
btnEn.pack(side=LEFT)

btnDe = Button(stegFrame, text='Decode File', command=decode)
btnDe.pack(side=LEFT)

#########
root.bind("<Return>", callback)
root.mainloop()
