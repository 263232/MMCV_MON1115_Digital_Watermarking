import tkinter as tk
from tkinter import filedialog, Text, simpledialog
import os
import numpy as np
import cv2
from PIL import Image, ImageTk

root = tk.Tk()
root.title('Digital Watermarking App')

def resize():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file to resize",
    filetypes=(("jpg","*.jpg"), ("png","*.png"), ("all files", "*.*")))
    img = cv2.imread(filename, 1)
    fx = simpledialog.askfloat("Enter the ratio","The ratio for x axis, value from range 0-1")
    fy = simpledialog.askfloat("Enter the ratio","The ratio for y axis, value from range 0-1")
    img_half = cv2.resize(img, (0, 0), fx=fx, fy=fy)
    path2 = filedialog.askdirectory(title="Select directory to save a file")
    os.chdir(path2)
    filename2 = simpledialog.askstring("Enter a file name","Include the extension (.jpg .png) in the file name")
    cv2.imwrite(filename2, img_half)

def compress():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file to compress",
                                          filetypes=(("png", "*.png"), ("jpg", "*.jpg"),  ("all files", "*.*")))
    picture = Image.open(filename)
    path2 = filedialog.askdirectory(title="Select directory to save a file")
    os.chdir(path2)
    filename2 = simpledialog.askstring("Enter a file name", "Include the extension (.jpg .png) in the file name")
    picture.save(filename2, optimize=True, quality=80)

canvas = tk.Canvas(root, height=600, width=400, bg="white")
canvas.grid(columnspan=3, rowspan=6)


#logo
logo = Image.open('logo2.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#instructions
instructions = tk.Label(root, text="Choose what you want to do with the photo", font="Raleway", bg="white")
instructions.grid(columnspan=3, column=0, row=1)

#frame = tk.Frame(root, bg="white")
#frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

resizeFile = tk.Button(root, text="Resize", font="Raleway", highlightcolor="#ff7000", fg="white", bg="orange", height=2, width=15, command=resize)
resizeFile.grid(column=1, row=2)

compressFile = tk.Button(root, text="Compress", font="Raleway", fg="white", bg="orange", height=2, width=15, command=compress)
compressFile.grid(column=1, row=3)

visibleWM = tk.Button(root, text="Visible WM", font="Raleway", fg="white", bg="orange", height=2, width=15)
visibleWM.grid(column=1, row=4)

invisibleVM = tk.Button(root, text="Invisible WM", font="Raleway", fg="white", bg="orange", height=2, width=15)
invisibleVM.grid(column=1, row=5)

root.mainloop()