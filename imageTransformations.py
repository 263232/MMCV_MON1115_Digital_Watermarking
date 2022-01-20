import cv2
import numpy as np


class ImageTransformations:

    @staticmethod
    def distortion(image_path):
        img = cv2.imread(image_path)

        A = img.shape[0] / 3.0
        w = 2.0 / img.shape[1]

        shift = lambda x: A * np.sin(2.0 * np.pi * x * w)

        for i in range(img.shape[1]):
            img[:, i] = np.roll(img[:, i], int(shift(i)))

        return img
