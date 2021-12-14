from PIL import Image
import cv2

class Steganography:

    @staticmethod
    def convert_int_to_binary(rgb):
        # Converting integer to a binary (string)
        r, g, b = rgb
        return (f'{r:08b}',
                f'{g:08b}',
                f'{b:08b}')

    @staticmethod
    def convert_binary_to_int(rgb):
        # Converting a binary (string) tuple to an integer tuple.
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def merge_rgb(rgb1, rgb2):
        # Merge two RGB tuples -> insert 4 most significant bits from signature
        # in the place of 4 least significant bits of image to being signatured
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:4],
               g1[:4] + g2[:4],
               b1[:4] + b2[:4])
        return rgb

    @staticmethod
    def merge(img1, img2):
        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = Steganography.convert_int_to_binary(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = Steganography.convert_int_to_binary((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = Steganography.convert_int_to_binary(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = Steganography.merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = Steganography.convert_binary_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = Steganography.convert_int_to_binary(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = Steganography.convert_binary_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image


def encoding_option():
    image_name = input("Enter image name to be signatured (with extension): ")
    image_name = image_name.strip()
    image = cv2.imread(image_name)
    print("The shape of the image is: ", image.shape)


    signature_name = input("Enter name of the image-signature (with extension): ")
    if len(signature_name) == 0:
        raise ValueError('Name not provided')
    else:
        image_signature = cv2.imread(signature_name)
        print("The shape of the signature is: ", image_signature.shape)

    encoded_image_filename = input("Enter the name of new encoded image(with extension): ")
    encoded_image = Steganography.merge(Image.open(image_name), Image.open(signature_name))
    encoded_image.save(encoded_image_filename)


def decoding_option(img, output):
    unmerged_image = Steganography.unmerge(Image.open(img))
    unmerged_image.save(output)

    image_name = input("Enter the name of the steganographed image that you want to decode (with extension): ")
    image_name = image_name.strip()
    image = cv2.imread(image_name)

    print("The Steganographed image is as shown: ")
    resized_image = cv2.resize(image, (500, 500))  # resize the original image as per your requirement
    cv2.imshow("Steganograpghed image", resized_image)  # display the Steganographed image

    decoded_signature_filename = input("Enter the name of the decoded image - signature (with extension): ")
    decoded_signature = Steganography.unmerge(Image.open(image_name))
    decoded_signature.save(decoded_signature_filename)


def steganography():
    a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: ")
    user_input = int(a)
    if user_input == 1:
        print("\nEncoding....")
        encoding_option()

    elif user_input == 2:
        print("\nDecoding....")
        decoding_option()
    else:
        raise Exception("Enter correct input")


if __name__ == '__main__':
    steganography()