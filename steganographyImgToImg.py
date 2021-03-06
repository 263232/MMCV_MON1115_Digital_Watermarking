from PIL import Image

class SteganographyImgToImg:

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
                rgb1 = SteganographyImgToImg.convert_int_to_binary(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = SteganographyImgToImg.convert_int_to_binary((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = SteganographyImgToImg.convert_int_to_binary(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = SteganographyImgToImg.merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = SteganographyImgToImg.convert_binary_to_int(rgb)

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
                r, g, b = SteganographyImgToImg.convert_int_to_binary(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = SteganographyImgToImg.convert_binary_to_int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image