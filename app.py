import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk

from steganographyImgToImg import SteganographyImgToImg
from steganographyTxtToImg import SteganographyTxtToImg
from imageTransformations import ImageTransformations
from steganographyDWTDCT import SteganographyDwtDct

root = tk.Tk()
root.title('Digital Watermarking App')


def resize():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file to resize",
                                          filetypes=(("png", "*.png"), ("all files", "*.*")))
    img = cv2.imread(filename, 1)
    fx = simpledialog.askfloat("Enter the ratio", "The ratio for x axis, value from range 0-1")
    fy = simpledialog.askfloat("Enter the ratio", "The ratio for y axis, value from range 0-1")
    img_half = cv2.resize(img, (0, 0), fx=fx, fy=fy)
    path2 = filedialog.askdirectory(title="Select directory to save a file")
    os.chdir(path2)
    filename2 = simpledialog.askstring("Enter a file name", "Include the extension (.jpg .png) in the file name")
    cv2.imwrite(filename2, img_half)

def compress():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file to compress",
                                          filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("all files", "*.*")))
    picture = Image.open(filename)
    path2 = filedialog.askdirectory(title="Select directory to save a file")
    os.chdir(path2)
    filename2 = simpledialog.askstring("Enter a file name", "Include the extension (.jpg .png) in the file name")
    picture.save(filename2, optimize=True, quality=50)

def distortion():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file to make distortion",
                                          filetypes=(("png", "*.png"), ("all files", "*.*")))
    distorted_image = ImageTransformations.distortion(filename)
    path2 = filedialog.askdirectory(title="Select directory to save a file")
    os.chdir(path2)
    distorted_image_path = simpledialog.askstring("Enter a file name",
                                                  "Include the extension (.jpg .png) in the file name")
    cv2.imwrite(distorted_image_path, distorted_image)




def scale(image, scale_width):
    (image_height, image_width) = image.shape[:2]
    new_height = int(scale_width / image_width * image_height)
    return cv2.resize(image, (scale_width, new_height))

def invisible_img_to_img_encode():
    image_name = filedialog.askopenfilename(initialdir="/",
                                            title="Enter image name to be signatured (with extension - have to  be "
                                                  ".jpg): ",
                                            filetypes=(("jpg", "*.jpg"), ("png", "*.png"), ("all files", "*.*")))
    image_name = image_name.strip()
    image = cv2.imread(image_name)
    print("The shape of the image is: ", image.shape)

    signature_name = filedialog.askopenfilename(initialdir="/",
                                                title="Enter name of the image-signature (with extension "
                                                      "- have to  be .jpg): ",
                                                filetypes=(
                                                    ("jpg", "*.jpg"), ("png", "*.png"),
                                                    ("all files", "*.*")))
    if len(signature_name) == 0:
        raise ValueError('Name not provided')
    else:
        image_signature = cv2.imread(signature_name)
        print("The shape of the signature is: ", image_signature.shape)

    encoded_image_filename = simpledialog.askstring("Enter a file name", "Include the extension (.png) in the "
                                                                         "file name")
    encoded_image = SteganographyImgToImg.merge(Image.open(image_name), Image.open(signature_name))
    encoded_image.save(encoded_image_filename)


def invisible_img_to_img_decode():
    image_name = filedialog.askopenfilename(initialdir="/", title="Enter the name of the steganographed image that "
                                                                  "you want to decode (with extension): ",
                                            filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("all files", "*.*")))
    image_name = image_name.strip()
    image = cv2.imread(image_name)

    print("The Steganographed image is as shown: ")
    resized_image = cv2.resize(image, (500, 500))  # resize the original image

    decoded_signature_filename = simpledialog.askstring("Enter a file name",
                                                        "Enter the name of the decoded image - signature (with "
                                                        "extension): ")
    decoded_signature = SteganographyImgToImg.unmerge(Image.open(image_name))
    decoded_signature.save(decoded_signature_filename)


def invisible_txt_to_img_encode():
    image_name = filedialog.askopenfilename(initialdir="/",
                                            title="Enter image name to be signatured (with extension - have to  be "
                                                  ".jpg): ",
                                            filetypes=(("jpg", "*.jpg"), ("png", "*.png"), ("all files", "*.*")))
    image = cv2.imread(image_name)

    print("The shape of the image is: ", image.shape)  # check the shape of image to calculate the number of bytes in it
    print("The original image is as shown: ")
    resized_image = cv2.resize(image, (500, 500))  # resize the image

    data = simpledialog.askstring("Enter a watermark", "Enter data (text) to be encoded")
    if len(data) == 0:
        raise ValueError('Data is empty')

    filename = simpledialog.askstring("Enter a file name", "Include the extension (.png) in the "
                                                           "file name")
    encoded_image = SteganographyTxtToImg.encode_message(image, data)  # hiding secret message into the selected image
    cv2.imwrite(filename, encoded_image)


def invisible_txt_to_img_decode():
    image_name = filedialog.askopenfilename(initialdir="/", title="Enter the name of the steganographed image that "
                                                                  "you want to decode (with extension): ",
                                            filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("all files", "*.*")))
    image_name = image_name.strip()
    image = cv2.imread(image_name)

    print("The Steganographed image is as shown: ")
    resized_image = cv2.resize(image, (500, 500))  # resize the original image

    text = SteganographyTxtToImg.decode_message(image)
    messagebox.showinfo("Decoded message", text)
    return text


def visible_sign():
    watermark_image_name = filedialog.askopenfilename(initialdir="/", title="Enter the name of the image - watermark",
                                                      filetypes=(
                                                          ("png", "*.png"), ("jpg", "*.jpg"), ("all files", "*.*")))
    watermark = scale(cv2.imread(watermark_image_name, cv2.IMREAD_UNCHANGED), 150)

    (watermark_height, watermark_width) = watermark.shape[:2]
    image_name = filedialog.askopenfilename(initialdir="/", title="Enter the name of the image you want to be signed",
                                            filetypes=(("jpg", "*.jpg"), ("png", "*.png"), ("all files", "*.*")))
    image = scale(cv2.imread(image_name), 900)
    (image_height, image_width) = image.shape[:2]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    overlay = np.zeros((image_height, image_width, 4), dtype='uint8')
    overlay[image_height - watermark_height:image_height, image_width - watermark_width:image_width] = watermark

    output1 = image.copy()
    output2 = image.copy()
    output3 = image.copy()
    cv2.addWeighted(overlay, 1.0, image, 1.0, 0, image)

    cv2.addWeighted(overlay, 0.1, image, 1.0, 0, output1)
    cv2.addWeighted(overlay, 0.5, image, 1.0, 0, output2)
    cv2.addWeighted(overlay, 1.0, image, 1.0, 0, output3)

    watermarked_filename = simpledialog.askstring("Enter a file name",
                                                  "Enter the name of the decoded image - signature (with "
                                                  "extension [png]): ")
    cv2.imwrite(watermarked_filename, image)


# ----------------------------------------------------------------------------------------------------------------------
canvas = tk.Canvas(root, height=900, width=800, bg="white")
canvas.grid(columnspan=3, rowspan=20)

# logo
logo = Image.open('logo2.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

# instructions
instructions = tk.Label(root, text="Choose what you want to do with the photo", font="Raleway", bg="white")
instructions.grid(columnspan=3, column=0, row=1)

# frame = tk.Frame(root, bg="white")
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
normalButtonWidthSize = 30
weiderButtonWidthSize = 45

resizeFile = tk.Button(root, text="Resize", font="Raleway", highlightcolor="#ff7000", fg="white", bg="orange", height=2,
                       width=normalButtonWidthSize, command=resize)
resizeFile.grid(column=1, row=2)

compressFile = tk.Button(root, text="Compress", font="Raleway", fg="white", bg="orange", height=2,
                         width=normalButtonWidthSize,
                         command=compress)
compressFile.grid(column=1, row=3)

distortionFile = tk.Button(root, text="Distortion", font="Raleway", fg="white", bg="orange", height=2,
                           width=normalButtonWidthSize,
                           command=distortion)
distortionFile.grid(column=1, row=4)

visibleWM = tk.Button(root, text="Visible WM", font="Raleway", fg="white", bg="orange", height=2,
                      width=normalButtonWidthSize, command=visible_sign)
visibleWM.grid(column=1, row=5)

invisibleVMImageEncode = tk.Button(root, text="Invisible WM (image as watermark) - encode", font="Raleway", fg="white",
                                   bg="orange", height=2, width=weiderButtonWidthSize,
                                   command=invisible_img_to_img_encode)
invisibleVMImageEncode.grid(column=1, row=6)

invisibleVMImageDecode = tk.Button(root, text="Invisible WM (image as watermark) - decode", font="Raleway", fg="white",
                                   bg="orange", height=2, width=weiderButtonWidthSize,
                                   command=invisible_img_to_img_decode)
invisibleVMImageDecode.grid(column=1, row=7)

invisibleVMTextEncode = tk.Button(root, text="Invisible WM (text as watermark) - encode", font="Raleway", fg="white",
                                  bg="orange", height=2, width=weiderButtonWidthSize,
                                  command=invisible_txt_to_img_encode)
invisibleVMTextEncode.grid(column=1, row=8)

invisibleVMTextDecode = tk.Button(root, text="Invisible WM (text as watermark) - decode", font="Raleway", fg="white",
                                  bg="orange", height=2, width=weiderButtonWidthSize,
                                  command=invisible_txt_to_img_decode)
invisibleVMTextDecode.grid(column=1, row=9)

invisibleVMDWTDCTTextEncode = tk.Button(root, text="Invisible WM DWT_DCT(image as watermark) - encode", font="Raleway",
                                        fg="white", bg="orange", height=2, width=weiderButtonWidthSize,
                                        command=SteganographyDwtDct.encode_watermark
                                        )
invisibleVMDWTDCTTextEncode.grid(column=1, row=10)

invisibleVMDWTDCTTextDecode = tk.Button(root, text="Invisible WM DWT_DCT (image as watermark) - decode", font="Raleway",
                                        fg="white", bg="orange", height=2, width=weiderButtonWidthSize,
                                        command=SteganographyDwtDct.decode_watermark
                                        )
invisibleVMDWTDCTTextDecode.grid(column=1, row=11)

root.mainloop()
