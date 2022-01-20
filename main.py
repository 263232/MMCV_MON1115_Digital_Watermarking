# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#   print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import cv2 as cv
import numpy as np


def scale(image, scale_width):
    (image_height, image_width) = image.shape[:2]
    new_height = int(scale_width / image_width * image_height)
    return cv.resize(image, (scale_width, new_height))


def visible():
    watermark = scale(cv.imread('images/logo.png', cv.IMREAD_UNCHANGED), 150)
    #watermark_ = cv.imread(args["watermark"], cv.IMREAD_UNCHANGED)
    #if args["correct"] > 0:
     #   (B, G, R, A) = cv.split(watermark_)
     #   B = cv.bitwise_and(B, B, mask=A)
     #   G = cv.bitwise_and(G, G, mask=A)
      #  R = cv.bitwise_and(R, R, mask=A)
      #  watermark = cv.merge([B, G, R, A])

    (watermark_height, watermark_width) = watermark.shape[:2]
    image = scale(cv.imread('images/road.jpg'), 900)
    (image_height, image_width) = image.shape[:2]
    image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

    overlay = np.zeros((image_height, image_width, 4), dtype='uint8')
    # overlay[0:watermark_height, 0:watermark_width] = watermark
    # overlay[0:watermark_height, image_width-watermark_width:image_width] = watermark
    overlay[image_height - watermark_height:image_height, image_width - watermark_width:image_width] = watermark

    output1 = image.copy()
    output2 = image.copy()
    output3 = image.copy()
    cv.addWeighted(overlay, 1.0, image, 1.0, 0, image)

    cv.addWeighted(overlay, 0.1, image, 1.0, 0, output1)
    cv.addWeighted(overlay, 0.5, image, 1.0, 0, output2)
    cv.addWeighted(overlay, 1.0, image, 1.0, 0, output3)

    cv.imwrite("WatermarkedImage.png", image)

    while True:
        cv.imshow("Overlay", overlay)
        cv.imshow("Image", image)
        cv.imshow("Watermark", watermark)

        cv.imshow("Overlay1", output1)
        cv.imshow("Image1", output2)
        cv.imshow("Watermark1", output3)

        if cv.waitKey(1) == ord('q'):
            break
if __name__ == '__main__':
    visible()