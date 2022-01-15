import cv2
import numpy as np


class SteganographyTxtToImg:

    @staticmethod
    def convert_pixel_to_binary(pixel):
        if type(pixel) == bytes or type(pixel) == np.ndarray:
            return [format(i, "08b") for i in pixel]
        elif type(pixel) == int or type(pixel) == np.uint8:
            return format(pixel, "08b")
        else:
            raise TypeError("Input type of pixel not supported")

    @staticmethod
    def convert_message_to_binary(message):
        if type(message) == str:
            return ''.join([format(ord(i), "08b") for i in message])
        elif type(message) == int or type(message) == np.uint8:
            return format(message, "08b")
        else:
            raise TypeError("Input type of message not supported")

    # Function to hide the secret message into the image
    @staticmethod
    def encode_message(image, secret_message):
        delimiter = "#####"  # the delimiter of the secret message

        n_bytes = image.shape[0] * image.shape[1] * 3 // 8  # maximum bytes to encode
        print("Maximum bytes to encode:", n_bytes)

        if len(secret_message) > n_bytes:
            raise ValueError("Message is too large, for given image")

        secret_message += delimiter  # adding delimiter to the end of the message to encode
        binary_secret_msg = SteganographyTxtToImg.convert_message_to_binary(secret_message)  # converting input data to binary format

        data_index = 0
        data_len = len(binary_secret_msg)  # length of data that needs to be hidden
        for values in image:
            for pixel in values:
                r, g, b = SteganographyTxtToImg.convert_pixel_to_binary(pixel)  # convert RGB values to binary format
                # modify the least significant bit only if there is still data to store
                if data_index < data_len:
                    # hide the data into least significant bit of red pixel
                    pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # hide the data into least significant bit of green pixel
                    pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # hide the data into least significant bit of  blue pixel
                    pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
                # if data is encoded, just break out of the loop
                if data_index >= data_len:
                    break

        return image

    @staticmethod
    def decode_message(image):
        delimiter = "#####"
        binary_data = ""
        for values in image:
            for pixel in values:
                r, g, b = SteganographyTxtToImg.convert_pixel_to_binary(pixel)  # converting the red,green and blue values into binary format
                binary_data += r[-1]  # extracting data from the least significant bit of red pixel
                binary_data += g[-1]  # extracting data from the least significant bit of green pixel
                binary_data += b[-1]  # extracting data from the least significant bit of blue pixel

        decoded_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]  # splitting by 8-bits
        decoded_data = ""
        for byte in decoded_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == delimiter:  # checking if reached the delimiter "#####"
                break

        return decoded_data[:-5]  # returning without the delimiter to show the original hidden message


def encoding_option():
    image_name = input("Enter image name(with extension): ")
    image = cv2.imread(image_name)

    print("The shape of the image is: ",
          image.shape)  # check the shape of image to calculate the number of bytes in it
    print("The original image is as shown: ")
    resized_image = cv2.resize(image, (500, 500))  # resize the image as per your requirement
    cv2.imshow("original image", resized_image)  # display the image

    data = input("Enter data to be encoded : ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    filename = input("Enter the name of new encoded image(with extension): ")
    encoded_image = SteganographyTxtToImg.encode_message(image, data)  # hiding secret message into the selected image
    cv2.imwrite(filename, encoded_image)


def decoding_option():
    image_name = input("Enter the name of the steganographed image that you want to decode (with extension): ")
    image_name = image_name.strip()
    image = cv2.imread(image_name)

    print("The Steganographed image is as shown: ")
    resized_image = cv2.resize(image, (500, 500))  # resize the original image as per your requirement
    cv2.imshow("Steganograpghed image", resized_image)  # display the Steganographed image

    text = SteganographyTxtToImg.decode_message(image)
    return text


def steganography():
    a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: ")
    user_input = int(a)
    if user_input == 1:
        print("\nEncoding....")
        encoding_option()

    elif user_input == 2:
        print("\nDecoding....")
        print("Decoded message is " + decoding_option())
    else:
        raise Exception("Enter correct input")


if __name__ == '__main__':
    steganography()
