import numpy as np
import pywt
import os
from PIL import Image
from scipy.fftpack import dct
from scipy.fftpack import idct
from tkinter import filedialog, Text, simpledialog, messagebox

current_path = str(os.path.dirname(__file__))

image = 'imagetest1.jpg'
watermark = 'wrcodetest1.png'


class SteganographyDwtDct:

    @staticmethod
    def convert_image(image_name, size, header):
        # img = Image.open('./pictures/' + image_name).resize((size, size), 1)

        img_path = filedialog.askopenfilename(initialdir="/", title=header,
                                              filetypes=(
                                                  ("png", "*.png"), ("jpg", "*.jpg"), ("all files", "*.*")))
        img = Image.open(img_path).resize((size, size), 1)
        img = img.convert('L')

        # img_save_location = simpledialog.askstring("Enter a file name",
        #                                               "Include the extension (.jpg .png) in the file name")
        img.save('./dwtDctTempDirectory/' + image_name)
        # img.save(img_save_location)

        image_array = np.array(img.getdata(), dtype=np.float).reshape((size, size))
        print
        image_array[0][0]
        print
        image_array[10][10]

        return image_array

    @staticmethod
    def process_coefficients(imArray, model, level):
        coeffs = pywt.wavedec2(data=imArray, wavelet=model, level=level)
        # print coeffs[0].__len__()
        coeffs_H = list(coeffs)

        return coeffs_H

    # def embed_mod2(coeff_image, coeff_watermark, offset=0):
    # #     for i in xrange(coeff_watermark.__len__()):
    # #         for j in xrange(coeff_watermark[i].__len__()):
    # #             coeff_image[i * 2 + offset][j * 2 + offset] = coeff_watermark[i][j]
    # #
    # #     return coeff_image
    # #
    # #
    # # def embed_mod4(coeff_image, coeff_watermark):
    # #     for i in xrange(coeff_watermark.__len__()):
    # #         for j in xrange(coeff_watermark[i].__len__()):
    # #             coeff_image[i * 4][j * 4] = coeff_watermark[i][j]
    # #
    # #     return coeff_image

    @staticmethod
    def embed_watermark(watermark_array, orig_image):
        watermark_array_size = watermark_array[0].__len__()
        watermark_flat = watermark_array.ravel()
        ind = 0

        for x in range(0, orig_image.__len__(), 8):
            for y in range(0, orig_image.__len__(), 8):
                if ind < watermark_flat.__len__():
                    subdct = orig_image[x:x + 8, y:y + 8]
                    subdct[5][5] = watermark_flat[ind]
                    orig_image[x:x + 8, y:y + 8] = subdct
                    ind += 1

        return orig_image

    @staticmethod
    def apply_dct(image_array):
        size = image_array[0].__len__()
        all_subdct = np.empty((size, size))
        for i in range(0, size, 8):
            for j in range(0, size, 8):
                subpixels = image_array[i:i + 8, j:j + 8]
                subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
                all_subdct[i:i + 8, j:j + 8] = subdct

        return all_subdct

    @staticmethod
    def inverse_dct(all_subdct):
        size = all_subdct[0].__len__()
        all_subidct = np.empty((size, size))
        for i in range(0, size, 8):
            for j in range(0, size, 8):
                subidct = idct(idct(all_subdct[i:i + 8, j:j + 8].T, norm="ortho").T, norm="ortho")
                all_subidct[i:i + 8, j:j + 8] = subidct

        return all_subidct

    @staticmethod
    def get_watermark(dct_watermarked_coeff, watermark_size):
        subwatermarks = []

        for x in range(0, dct_watermarked_coeff.__len__(), 8):
            for y in range(0, dct_watermarked_coeff.__len__(), 8):
                coeff_slice = dct_watermarked_coeff[x:x + 8, y:y + 8]
                subwatermarks.append(coeff_slice[5][5])

        watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size)

        return watermark

    @staticmethod
    def recover_watermark(image_array, model='haar', level=1):
        coeffs_watermarked_image = SteganographyDwtDct.process_coefficients(image_array, model, level=level)
        dct_watermarked_coeff = SteganographyDwtDct.apply_dct(coeffs_watermarked_image[0])

        watermark_array = SteganographyDwtDct.get_watermark(dct_watermarked_coeff, 128)

        watermark_array = np.uint8(watermark_array)

        # Save result
        img = Image.fromarray(watermark_array)
        recovered_watermark_file_name = simpledialog.askstring("Enter a file name for decoded watermark",
                                                               "Include the extension (.jpg) in the file name")
        img.save(recovered_watermark_file_name)

    @staticmethod
    def recover_watermark_decoding_file(image_array, model='haar', level=1):
        image_array = image_array.resize((2048, 2048), 1)
        image_array = image_array.convert('L')

        # image_array = np.array(img.getdata(), dtype=np.float).reshape((size, size))

        coeffs_watermarked_image = SteganographyDwtDct.process_coefficients(image_array, model, level=level)
        dct_watermarked_coeff = SteganographyDwtDct.apply_dct(coeffs_watermarked_image[0])

        watermark_array = SteganographyDwtDct.get_watermark(dct_watermarked_coeff, 128)

        watermark_array = np.uint8(watermark_array)

        # Save result
        img = Image.fromarray(watermark_array)
        path2 = filedialog.askdirectory(title="Select directory to save a file")
        os.chdir(path2)
        recovered_watermark_file_name = simpledialog.askstring("Enter a file name for decoded watermark",
                                                               "Include the extension (.jpg) in the file name")
        img.save(recovered_watermark_file_name)

    @staticmethod
    def print_image_from_array(image_array):
        image_array_copy = image_array.clip(0, 255)
        image_array_copy = image_array_copy.astype("uint8")
        img = Image.fromarray(image_array_copy)
        watermarked_file_name = simpledialog.askstring("Enter a file name for watermarked image",
                                                       "Include the extension (.jpg) in the file name")
        img.save("./results/" + watermarked_file_name)

    @staticmethod
    def encode_watermark():
        model = 'haar'
        level = 1
        image_array = SteganographyDwtDct.convert_image(image, 2048, "Enter the name of the image to be watermarked")
        watermark_array = SteganographyDwtDct.convert_image(watermark, 128, "Enter the name of  image - watermark")

        coeffs_image = SteganographyDwtDct.process_coefficients(image_array, model, level=level)
        dct_array = SteganographyDwtDct.apply_dct(coeffs_image[0])
        dct_array = SteganographyDwtDct.embed_watermark(watermark_array, dct_array)
        coeffs_image[0] = SteganographyDwtDct.inverse_dct(dct_array)

        # reconstruction
        image_array_H = pywt.waverec2(coeffs_image, model)
        SteganographyDwtDct.print_image_from_array(image_array_H)

        # recover images
        SteganographyDwtDct.recover_watermark(image_array=image_array_H, model=model, level=level)

    @staticmethod
    def decode_watermark():
        model = 'haar'
        level = 1
        img_path = filedialog.askopenfilename(initialdir="/", title="Enter the name of the image to decode watermarked",
                                              filetypes=(
                                                  ("jpg", "*.jpg"), ("png", "*.png"), ("all files", "*.*")))
        image_array_H = Image.open(img_path)
        SteganographyDwtDct.recover_watermark_decoding_file(image_array=image_array_H, model=model, level=level)

# SteganographyDwtDct.w2d()
