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
scan_lines_loaded  = []
scan_lines_current = []

################################################################################

def brz(x0, y0, x1, y1):
    print "Bresenham's line algorithm"
    pixels = image_temp.load()

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            #self.set(x, y)
            try:
                pixels[x,y] = (255,0,0)
            except Exception:
                print 'pixels ' + str(x) + ' ' + str(y) + ' out of bounds'
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            #self.set(x, y)
            try:
                pixels[x,y] = (255,0,0)
            except Exception:
                print 'pixels ' + str(x) + ' ' + str(y) + ' out of bounds'
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    #self.set(x, y)
    try:
        pixels[x,y] = (255,0,0)
    except Exception:
        print 'pixels ' + str(x) + ' ' + str(y) + ' out of bounds'

    wline = ImageTk.PhotoImage(image_temp)
    panel.configure(image=wline)
    panel.image = wline

################################################################################

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
ent.insert(END,'filename')
ent.pack(side=LEFT)

ent_arg = Entry(loadFrame)
ent_arg.insert(END,'arg')
ent_arg.pack(side=LEFT)

def callback():
    file_name = ent.get()
    print 'trying to load: ' + str(file_name)

    image = Image.open(file_name)
    shutil.copy(file_name,file_name + '.temp.jpg')
    image_temp = Image.open(file_name + '.temp.jpg')

    img2 = ImageTk.PhotoImage(image_temp)
    panel.configure(image=img2)
    panel.image = img2

    global scan_lines_loaded
    global scan_lines_current
    scan_lines_loaded = []
    scan_lines_current = []

def saver():
    print 'saving edits to ' + file_name + ' as ' + file_name + '.temp.jpg'
    image_temp.save(file_name + '.temp.jpg')

def loadscan():
    global scan_lines_loaded
    global scan_lines_current
    scan_lines_loaded = []
    scan_lines_current = []
    file_to_load = str(ent.get())
    arg = str(ent_arg.get())
    num = 1
    adder = 1
    if (arg == ''):
        print 'no arg'
        adder = 0
    else:
        arg = int(arg)
    print 'loading scanline file ... ' + file_to_load + ' with arg ' + str(arg)
    f = open(file_to_load, 'r')
    for line in f:
        if (num > arg and adder == 1):
            break
        points = line.split(" ")
        x_1 = int(points[0])
        y_1 = int(points[1])
        x_2 = int(points[2])
        y_2 = int(points[3])
        brz(x_1,y_1,x_2,y_2)
        scan_lines_loaded.append([x_1,y_1,x_2,y_2])
        scan_lines_current.append([x_1,y_1,x_2,y_2])
        num = num + adder
    return arg

def updatescanlines():
    global scan_lines_current
    global image
    global image_temp
    image = Image.open(file_name)
    shutil.copy(file_name,file_name + '.temp.jpg')
    image_temp = Image.open(file_name + '.temp.jpg')
    img3 = ImageTk.PhotoImage(image_temp)
    panel.configure(image=img3)
    panel.image = img3
    print 'updating scanlines... '
    for points in scan_lines_current:
        x_1 = int(points[0])
        y_1 = int(points[1])
        x_2 = int(points[2])
        y_2 = int(points[3])
        brz(x_1,y_1,x_2,y_2)
    return 0

def savescan():
    file_to_save = str(ent.get())
    arg = str(ent_arg.get())
    num = 1
    adder = 1
    write_string = ''
    if (arg == ''):
        print 'no arg'
        adder = 0
    else:
        arg = int(arg)
    print 'saving scanline file ... ' + file_to_save + ' with arg ' + str(arg)
    f = open(file_to_save, 'w+')
    print len(scan_lines_current)
    for scanline in scan_lines_current:
        if (num > arg and adder == 1):
            break
        f.write(str(scanline[0]) + ' ' + str(scanline[1]) + ' ' + str(scanline[2]) + ' ' + str(scanline[3]) + '\n')
        num = num + adder
    return arg


####### NOTE loading scanfile done, NOTE finish save scan

btnEnter = Button(loadFrame, text='Load Image File', command=callback)
btnEnter.pack(side=LEFT)

btnSave = Button(loadFrame, text='Save Image File', command=saver)
btnSave.pack(side=LEFT)

btnLdSc = Button(loadFrame, text='Load Scanline File', command=loadscan)
btnLdSc.pack(side=LEFT)

btnSvSc = Button(loadFrame, text='Save Scanline File', command=savescan)
btnSvSc.pack(side=LEFT)

######## Draw a line NOTE: DONE!

lineFrame = Frame(width=600)
lineFrame.pack()

lineLabel = Label(lineFrame,text='line drawer')
lineLabel.pack(side=LEFT)
x1 = Entry(lineFrame, text='x1')
x1.insert(END,'x1')
x1.pack(side=LEFT)
y1 = Entry(lineFrame, text='y1')
y1.insert(END,'y1')
y1.pack(side=LEFT)
x2 = Entry(lineFrame, text='x2')
x2.insert(END,'x2')
x2.pack(side=LEFT)
y2 = Entry(lineFrame, text='y2')
y2.insert(END,'y2')
y2.pack(side=LEFT)

def drawer():
    print 'drawing... ' + '(' + str(x1.get()) + ',' + str(y1.get()) + '),' + '(' + str(x2.get()) + ',' + str(y2.get()) + ')'
    brz(int(x1.get()),int(y1.get()),int(x2.get()),int(y2.get()))
    scan_lines_current.append([int(x1.get()),int(y1.get()),int(x2.get()),int(y2.get())])

btnDraw = Button(lineFrame, text='Draw', command=drawer)
btnDraw.pack(side=LEFT)

######## NOTE basic Translate works, NOTE basic Scale works

basicFrame = Frame(width=600)
basicFrame.pack()

basicLabel = Label(basicFrame,text='Basic Translate / Basic Scale')
basicLabel.pack(side=LEFT)
x_b = Entry(basicFrame, text='Tx/Sx')
x_b.insert(END, 'Tx/Sx')
x_b.pack(side=LEFT)
y_b = Entry(basicFrame, text='Ty/Sy')
y_b.insert(END, 'Ty/Sy')
y_b.pack(side=LEFT)

def basictranslate():
    print 'basic translating... '
    x_guy = int(x_b.get())
    y_guy = int(y_b.get())
    global scan_lines_current
    print scan_lines_current
    for i in range(0,len(scan_lines_current)):
        scan_lines_current[i][0] = scan_lines_current[i][0] + x_guy
        scan_lines_current[i][1] = scan_lines_current[i][1] + y_guy
        scan_lines_current[i][2] = scan_lines_current[i][2] + x_guy
        scan_lines_current[i][3] = scan_lines_current[i][3] + y_guy
    print scan_lines_current
    updatescanlines()

def basicscale():
        print 'baisc scaling... '
        x_guy = float(x_b.get())
        y_guy = float(y_b.get())
        global scan_lines_current
        print scan_lines_current
        for i in range(0,len(scan_lines_current)):
            scan_lines_current[i][0] = int(scan_lines_current[i][0] * x_guy)
            scan_lines_current[i][1] = int(scan_lines_current[i][1] * y_guy)
            scan_lines_current[i][2] = int(scan_lines_current[i][2] * x_guy)
            scan_lines_current[i][3] = int(scan_lines_current[i][3] * y_guy)
        print scan_lines_current
        updatescanlines()

btnBasct = Button(basicFrame, text='Apply Translate', command=basictranslate)
btnBasct.pack(side=LEFT)
btnBascs = Button(basicFrame, text='Apply Scale', command=basicscale)
btnBascs.pack(side=LEFT)

######### NOTE Scale

scaleFrame = Frame(width=600)
scaleFrame.pack()

scaleLabel = Label(scaleFrame,text='Scale')
scaleLabel.pack(side=LEFT)
sx = Entry(scaleFrame)
sx.insert(END,'Sx')
sx.pack(side=LEFT)
sy = Entry(scaleFrame)
sy.insert(END,'Sy')
sy.pack(side=LEFT)
cx = Entry(scaleFrame)
cx.insert(END,'Cx')
cx.pack(side=LEFT)
cy = Entry(scaleFrame)
cy.insert(END,'Cy')
cy.pack(side=LEFT)

def scale():
    print 'scaling... '
    x_guy = float(cx.get())
    y_guy = float(cy.get())
    global scan_lines_current
    x_dude = float(sx.get())
    y_dude = float(sy.get())
    for i in range(0,len(scan_lines_current)):
        scan_lines_current[i][0] = int(scan_lines_current[i][0] * x_dude)
        scan_lines_current[i][1] = int(scan_lines_current[i][1] * y_dude)
        scan_lines_current[i][2] = int(scan_lines_current[i][2] * x_dude)
        scan_lines_current[i][3] = int(scan_lines_current[i][3] * y_dude)
    for i in range(0,len(scan_lines_current)):
        scan_lines_current[i][0] = int(scan_lines_current[i][0] + x_guy)
        scan_lines_current[i][1] = int(scan_lines_current[i][1] + y_guy)
        scan_lines_current[i][2] = int(scan_lines_current[i][2] + x_guy)
        scan_lines_current[i][3] = int(scan_lines_current[i][3] + y_guy)
    print scan_lines_current
    print scan_lines_current
    updatescanlines()

btnScale = Button(scaleFrame, text='Apply', command=scale)
btnScale.pack(side=LEFT)

######### NOTE Rotate NOTE basic Rotate

rotateFrame = Frame(width=600)
rotateFrame.pack()

rotLabel = Label(rotateFrame,text='Rotate')
rotLabel.pack(side=LEFT)
angle = Entry(rotateFrame, text='angle')
angle.insert(END,'angle')
angle.pack(side=LEFT)
rot_cx = Entry(rotateFrame)
rot_cx.insert(END,'Cx')
rot_cx.pack(side=LEFT)
rot_cy = Entry(rotateFrame)
rot_cy.insert(END,'Cy')
rot_cy.pack(side=LEFT)

def basicrotate():
    angle_val = math.radians(float(angle.get()))
    for i in range(0,len(scan_lines_current)):
        px1 = float(scan_lines_current[i][0])
        py1 = float(scan_lines_current[i][1])
        px2 = float(scan_lines_current[i][2])
        py2 = float(scan_lines_current[i][3])

        qx1 = math.cos(angle_val) * px1 - math.sin(angle_val) * py1
        qy1 = math.sin(angle_val) * px1 + math.cos(angle_val) * py1
        qx2 = math.cos(angle_val) * px2 - math.sin(angle_val) * py2
        qy2 = math.sin(angle_val) * px2 + math.cos(angle_val) * py2

        scan_lines_current[i][0] = int(qx1)
        scan_lines_current[i][1] = int(qy1)
        scan_lines_current[i][2] = int(qx2)
        scan_lines_current[i][3] = int(qy2)
    print scan_lines_current
    updatescanlines()

def rotate():
    ox = float(rot_cx.get())
    oy = float(rot_cy.get())
    angle_val = math.radians(float(angle.get()))
    for i in range(0,len(scan_lines_current)):
        px1 = float(scan_lines_current[i][0])
        py1 = float(scan_lines_current[i][1])
        px2 = float(scan_lines_current[i][2])
        py2 = float(scan_lines_current[i][3])

        qx1 = ox + math.cos(angle_val) * (px1 - ox) - math.sin(angle_val) * (py1 - oy)
        qy1 = oy + math.sin(angle_val) * (px1 - ox) + math.cos(angle_val) * (py1 - oy)
        qx2 = ox + math.cos(angle_val) * (px2 - ox) - math.sin(angle_val) * (py2 - oy)
        qy2 = oy + math.sin(angle_val) * (px2 - ox) + math.cos(angle_val) * (py2 - oy)

        scan_lines_current[i][0] = int(qx1)
        scan_lines_current[i][1] = int(qy1)
        scan_lines_current[i][2] = int(qx2)
        scan_lines_current[i][3] = int(qy2)
    print scan_lines_current
    updatescanlines()

btnRotateb = Button(rotateFrame, text='Apply Basic Rotate', command=basicrotate)
btnRotateb.pack(side=LEFT)
btnRotate = Button(rotateFrame, text='Apply Rotate', command=rotate)
btnRotate.pack(side=LEFT)

######### TODO Matrix Transform

matFrame = Frame(width=600)
matFrame.pack()

matLabel = Label(matFrame,text='Apply Matrix Transform')
matLabel.pack(side=LEFT)
matrix = Entry(matFrame, text='matrix')
matrix.insert(END,'matrix')
matrix.pack(side=LEFT)
mat_dl = Entry(matFrame, text='Datalines')
mat_dl.insert(END,'Datalines')
mat_dl.pack(side=LEFT)
btnMatTfm = Button(matFrame, text='Apply')
btnMatTfm.pack(side=LEFT)

######### TODO display pix

iodFrame = Frame(width=600)
iodFrame.pack()

iodLabel = Label(iodFrame,text='Dispaly Scanlines')
iodLabel.pack(side=LEFT)
iod_dl = Entry(iodFrame, text='datalines')
iod_dl.insert(END,'datalines')
iod_dl.pack(side=LEFT)
iod_num = Entry(iodFrame, text='num')
iod_num.insert(END,'num')
iod_num.pack(side=LEFT)
btnIOD3 = Button(iodFrame, text='Apply DisplayPixels')
btnIOD3.pack(side=LEFT)

#########

root.bind("Q", scale)
root.bind("S", basictranslate)
root.bind("A", basicscale)
root.bind("D", drawer)
root.bind("<Return>", callback)
root.mainloop()
