import cv2
import numpy as np

class ImageTransformations:
    def distortion(imagePath):
        img = cv2.imread(imagePath)

        A = img.shape[0] / 3.0
        w = 2.0 / img.shape[1]

        shift = lambda x: A * np.sin(2.0 * np.pi * x * w)

        for i in range(img.shape[1]):
            img[:, i] = np.roll(img[:, i], int(shift(i)))

        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        return img
