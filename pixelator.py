from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.cluster import KMeans
from matplotlib.image import imread


def pixelate(image, new_width, new_height, num_colours):
    original_image = Image.open(image)
    width, height = original_image.size

    # getting the size of the blocks
    blk_width = width//new_width
    blk_height = height//new_height
    blk_size = blk_width * blk_height

    # cropping the image so the blocks fit
    image_cropped = original_image.crop((0, 0, (width-(width % new_width)), (height-(height % new_height))))

    # create a new image for the pixelated version and ensuring the modes are both RGB
    image_mode = image_cropped.mode
    pixelated_image = Image.new("RGB", image_cropped.size)

    width, height = image_cropped.size
    if image_mode != "RGB":
        image_rgb = image_cropped.convert("RGB")
    else:
        image_rgb = image_cropped

    # iterating through the pixels in each block
    for x1 in range(0, width, blk_width):
        for y1 in range(0, height, blk_height):
            red_sum = 0
            green_sum = 0
            blue_sum = 0
            for y in range(y1, blk_height + y1):
                for x in range(x1, blk_width + x1):

                    # adding to the sums of the colours from the RGB values of each pixel
                    red_sum += image_rgb.getpixel((x, y))[0]
                    green_sum += image_rgb.getpixel((x, y))[1]
                    blue_sum += image_rgb.getpixel((x, y))[2]

            # finding the average of the RGB values and setting the block to the average
            red_av = red_sum//blk_size
            green_av = green_sum//blk_size
            blue_av = blue_sum//blk_size

            for y in range(y1, blk_height + y1):
                for x in range(x1, blk_width + x1):
                    pixelated_image.putpixel((x, y), (red_av, green_av, blue_av))

    # saving the pixelated image and using it to call the compression function
    new_name = "pixelated_" + image
    pixelated_image.save(new_name)
    pixelated_image = imread(new_name)
    compress_colours(image, num_colours, pixelated_image)


# this function takes the pixelated image and does colour compression on it using k-means clustering
def compress_colours(image, num_colours, pixelated_image):
    # reducing numbers in image by dividing by 255
    compressed_image = pixelated_image
    compressed_image = compressed_image/255.0

    # flattening the image into a 2D array
    flattened = np.reshape(compressed_image, (compressed_image.shape[0] * compressed_image.shape[1],
                                              compressed_image.shape[2]))

    # clustering, recolouring the pixels and reshaping the image
    clusters = KMeans(n_clusters=num_colours)
    clusters.fit(flattened)
    coloured = clusters.cluster_centers_
    coloured = coloured[clusters.labels_]
    coloured = coloured.reshape(pixelated_image.shape)

    # saving and showing the final image
    plt.imsave('final_'+image, coloured)
    im = Image.open('final_'+image)
    im.show()

# error handling for input
if len(sys.argv) != 5:
    print("Please try again. The proper format is 'python pixelator.py image desired_width desired_height'")
else:
    pixelate(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
