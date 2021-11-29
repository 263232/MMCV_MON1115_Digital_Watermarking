# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
 #   print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import numpy as np
import cv2 as cv

def scale(image,scale_width):
    (image_height, image_width) = image.shape[:2]
    new_height = int(scale_width /image_width *image_height)
    return cv.resize(image,(scale_width, new_height))

watermark = scale(cv.imread('images/logo.png'),150)
(watermark_height, watermark_width)=watermark.shape[:2]
image = scale(cv.imread('images/road.jpg'),1000)
(image_height, image_width)=image.shape[:2]
image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)


while True:
    cv.imshow("Image", image)
    cv.imshow("Watermark", watermark)
    if cv.waitKey(1) == ord('q'):
        break



