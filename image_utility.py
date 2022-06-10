import glob as gl
import random
import string
from PIL import Image

# Keep Aspect Ratio
# https://stackoverflow.com/questions/2232742/does-python-pil-resize-maintain-the-aspect-ratio

def random_color_string():
    # create tuple of three random numbers between (001 and 999)
    return tuple(random.sample(range(0, 255), 3))
    
    
def random_color():
    return ['red', 'blue', 'green', 'orange', 'skyblue', 'grey', 'lightgrey',
            'white']
    

def build_images():
    # return a list of random images
    # List Comprehension-- [do_thing() for range condition]
    return [Image.new(mode="RGB", size=(600, 800), color='red')\
            for n in range(10)]


def merge_images(image1, image2):
    # Compare and resize image to match small of the 2
    # find small, reduce large image to it's size --
    # do this in *one* line of code
    # get height, width of image
    large_img, small_img = compare_image_sizes(image1, image2)
    large_img = large_img.resize((small_img.height, small_img.width))
    new_image = Image.new('RGB', (2*small_img.size[0], small_img.size[1]),
                                 (250, 250, 250))
    new_image.paste(small_img, (0, 0))
    new_image.paste(large_img, (small_img.size[0], 0))
    return new_image


def compare_image_sizes(image1, image2):
    # Args: 2 Image Files
    # Returns -- 1st larger image, 2nd smaller image
    larger_image = max(image1.Image.size, image2.Image.size)
    smaller_image = min(image1.Image.size, image2.Image.size)
    return larger_image, smaller_image


def generate_ranstring():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(10))
    return str(result_str)


# Needs to have a working directory confirmed
def list_images():
    files = gl.glob('*.png') + gl.glob('*.gif') + gl.glob('*.jpg')
    return files


def random_image(filelist):
    return random.choice(filelist)


print(random_color())
im_list = build_images()
