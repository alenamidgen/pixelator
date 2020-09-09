from PIL import Image
import sys


#the go function takes the name of an image the user wants to pixelate, and the new width and height, which are the number of pixels the user wants the new image to have
def go(image, new_width, new_height):
    original_image = Image.open(image)
    width, height = original_image.size

    # getting the size of the blocks, where each block represents a pixel, but it large enough for the user to see it without zooming in
    blk_width = width//new_width
    blk_height = height//new_height
    blk_size = blk_width * blk_height

    # cropping the original image so the blocks fit
    image_cropped = original_image.crop((0, 0, (width-(width % new_width)), (height-(height % new_height))))

    # creating a new image for the pixelated version and ensuring the modes are both RGB
    image_mode = image_cropped.mode
    pixelated_image = Image.new("RGB", image_cropped.size)
    if image_mode != "RGB":
        image_rgb = image_cropped.convert("RGB")
    else:
        image_rgb = image_cropped

    # looping through each block    
    for x1 in range(0, width, blk_width):
        for y1 in range(0, height, blk_height):
            #setting variables representing the sum of the RGB colour values to 0, since they must reset after each block
            red_sum = 0
            green_sum = 0
            blue_sum = 0
            #iterating through pixels in each block
            for y in range(y1, blk_height + y1):
                for x in range(x1, blk_width + x1):
                    #adding the RGB values of each pixel to the seperate colour sums
                    red_sum += image_rgb.getpixel((x, y))[0]
                    green_sum += image_rgb.getpixel((x, y))[1]
                    blue_sum += image_rgb.getpixel((x, y))[2]
            
            #finding the average of each RGB value
            red_av = red_sum//blk_size
            green_av = green_sum//blk_size
            blue_av = blue_sum//blk_size

            # iterating through the pixels in the block again, this time setting each pixel of the new image to the RGB average 
            for y in range(y1, blk_height + y1):
                for x in range(x1, blk_width + x1):
                    pixelated_image.putpixel((x, y), (red_av, green_av, blue_av))

    #lastly, the program shows the new image, and saves it 
    pixelated_image.show()
    new_name = "pixelated_" + image
    pixelated_image.save(new_name)


# the right number and format of arguments must be written for the program to run the go function
if len(sys.argv) != 4:
    print("Please try again. The proper format is 'python pixelator.py image desired_width desired_height'")
else:
    go(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
