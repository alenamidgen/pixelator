from PIL import Image
import sys


def go(image, new_width, new_height):
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
    if image_mode != "RGB":
        image_rgb = image_cropped.convert("RGB")
    else:
        image_rgb = image_cropped

    for x1 in range(0, width, blk_width):
        for y1 in range(0, height, blk_height):
            red_sum = 0
            green_sum = 0
            blue_sum = 0
            for y in range(y1, blk_height + y1):
                for x in range(x1, blk_width + x1):
                    red_sum += (image_rgb.getpixel((x, y)))[0]
                    green_sum += image_rgb.getpixel((x, y))[1]
                    blue_sum += image_rgb.getpixel((x, y))[2]

            red_av = red_sum//blk_size
            green_av = green_sum//blk_size
            blue_av = blue_sum//blk_size

            for y in range(y1, blk_height + y1):
                for x in range(x1, blk_width + x1):
                    pixelated_image.putpixel((x, y), (red_av, green_av, blue_av))

    pixelated_image.show()
    new_name = "pixelated_" + image
    pixelated_image.save(new_name)


if len(sys.argv) != 4:
    print("Please try again. The proper format is 'python pixelator.py image desired_width desired_height'")
else:
    go(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
