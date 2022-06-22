import base64
import os
import io
import itertools
import random
import PySimpleGUI as sg
from PIL import Image
import glob as gl
import string

# TO DO -- Set Up Enable Events to toggle between Web and Local layouts
# Task 6/21/22 - Get Previous Image to take Current Image Index and subtract 1
#       for path in previous_images:
#           if previous_images[path] == path of ... ?
#               current_img_path = path
# 6/22/22 -- Set Up Conditionals for JPGs
#       if image.endswith('jpg') or image.endswith('jpeg'):
#           create new folder (check if it exists)
#           add folder to current_path_ + 'side'
#           save copy of image as png
#

# DEFINE VARIABLES
export_folder = r'.'
ref_folder_l = r'.'
ref_folder_r = r'.'

extensions = ['gif', 'png', 'jpg', 'jpeg']
files_l = [os.path.join(ref_folder_l, l) for l in os.listdir(ref_folder_l) if l.endswith(tuple(extensions))]
files_r = [os.path.join(ref_folder_r, r) for r in os.listdir(ref_folder_r) if r.endswith(tuple(extensions))]

# Previous Image Functionality
prev_imgs_l = []
prev_imgs_r = []


current_img_path_l = None
current_img_path_r = None


MAX_DIMENSIONS = (120, 160)

# --- REROLL FUNCTIONS
def format_image_to_display(input_file, size=MAX_DIMENSIONS):
    image = Image.open(input_file)
    width, height = image.size
    new_width, new_height = size
    if new_width != width or new_height != height:  # if the requested size is different than original size
        scale = min(new_height / height, new_width / width)
        resized_image = image.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
    else:
        resized_image = image

    with io.BytesIO() as bio:
        resized_image.save(bio, format='PNG')
        contents = bio.getvalue()
        encoded = base64.b64encode(contents)
    return encoded


def randomize_image(files, prev_images):
    image = random.choice(files)
    while image in prev_images:
        image = random.choice(files)
    return image


def reroll(lock, files, prev_imgs, current_img_path, window_key):
    if values[lock] is False:
        image = randomize_image(files, prev_imgs)
        current_img_path = image
        image = format_image_to_display(image, MAX_DIMENSIONS)
        print(type(image))
        window[window_key].update(data = image)
        prev_imgs.append(image)      #append current image to previous images list
        print(current_img_path)



# FUNCTIONS
# --- REROLL FUNCTIONS
def generate_ranstring():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(10))
    return str(result_str)

def compare_image_sizes(image1, image2):
    # Args: 2 Image Files
    # Returns -- 1st larger image, 2nd smaller image
    larger_image = max(image1.Image.size, image2.Image.size)
    smaller_image = min(image1.Image.size, image2.Image.size)
    return larger_image, smaller_image


def export_image(merged_image):
    merged_image.Image.save(export_folder + "img_" + generate_ranstring() + ".jpg", "JPEG")


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


# Layout Generator Functions
def img_buttons(justify):
    if justify == 'L':
        return[ [sg.Button('<<< Previous Image', k='-L-PREVIOUS-'),
                 sg.Checkbox(text='Lock', k='-L-LOCK-')] ]
    elif justify == 'R':
        return [ [sg.Checkbox(text='Lock', k='-R-LOCK-'),
                 sg.Button('Previous Image >>>', k='-R-PREVIOUS-')] ]

# TO DO -- Break Reference Folders into 2, -L-REF-FOLDER- and -R-REF-FOLDER-
def source_column():
    return [ [sg.Radio('Local', 1, k='-LOCAL-RADIO-', default=True),
             sg.Text('Left Source:'),
             sg.InputText(k='L-REF-FOLDER-'), sg.FolderBrowse(k='L-REF-BROWSE-')],
            # TO DO enable events -- toggle between Local and Web setups
            [sg.Radio('Web ', 1, k='-WEB-RADIO'),
             sg.Text('Right Source:', size=(15, 1)),
             sg.InputText(k='R-REF-FOLDER-'),
             sg.FolderBrowse(k='R-REF-BROWSE')] ]


def image_element(side):
    return [ [sg.Image(k = '-' + side + '-IMAGE-',
            background_color = 'Light Grey', size=MAX_DIMENSIONS)] ]


# TO DO -- Add Individual Ref Folders and Thumbnails of Previous Images
def column_img(side):
    return [ [sg.Column(img_buttons(side), justification='center')],
            [sg.Column(image_element(side), justification='center')],
            [sg.Input(default_text='', k = '-' + side + '-IMG-TAGS')] ]


def reroll_button():
    return [[sg.Button('-REROLL-')]]


def export_column():
    return [[sg.Text('Export:'), sg.InputText(k='-EXPORT-FOLDER-'),
            sg.FolderBrowse(), sg.Button('Export')]]


def unpack(nested_list):
    unpacked_list = list(itertools.chain(*nested_list))
    return unpacked_list

# Make a button mapped to the dir() function
layout = [  [sg.Button('Debug', k = '-DEBUG-')],
            [sg.Column(source_column(), justification='center')],
            [sg.Column(column_img('L'), justification='left'), sg.Column(reroll_button()), sg.Column(column_img('R'), justification='right')],
            [sg.Column(export_column(), justification='center')],
            [sg.Button('Exit', k = '-EXIT-')]
         ]


window = sg.Window('Random Image Selector', layout = layout)


# Event Loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-DEBUG-':
      for item in prev_imgs_l:
        print(item)
      for item in prev_imgs_r:
        print(item)

    if event == '-L-PREVIOUS-':
        #find current index, subtract one from it, display that item
        print(f'Current Image Path: {prev_imgs_l.index(current_img_path_l)}')
        current_index_l = prev_imgs_l.index(current_img_path_l)
        print(current_index_l)
        window['-L-IMAGE-'].update(prev_imgs_l[current_index_l - 1])
        print("Key '-L-Previous-'")

    # TO DO--Convert "window[]" to find current image in list
    if event == '-R-PREVIOUS-':
        current_index_r = prev_imgs_r.index(current_img_path_r)
        print(current_index_r)
        window['-R-IMAGE-'].update(prev_imgs_r[current_index_r - 1])
        print("Key '-R-Previous-'")


    if event == '-REROLL-':
        print("Key '-REROLL-'")

        # Set reference folder to the new folder
        # window['ref_folder'].update(ref_folder)
        reroll('-L-LOCK-', files_l, prev_imgs_l, current_img_path_l, '-L-IMAGE-')
        reroll('-R-LOCK-', files_r, prev_imgs_r, current_img_path_r, '-R-IMAGE-')
        '''
        if values['-L-LOCK-'] is False:
            rolled_img_l = random.choice(files_l)
            current_img_path_l = rolled_img_l
            while rolled_img_l in prev_imgs_l:
                rolled_img_l = random.choice(files_l)
            window['-L-IMAGE-'].update(rolled_img_l)
            prev_imgs_l.append(rolled_img_l)      #append current image to previous images list
            print(current_img_path_l)


        if values['-R-LOCK-'] is False:
            rolled_img_r = random.choice(files_r)
            current_img_path_r = rolled_img_r
            while rolled_img_r in prev_imgs_r:
                rolled_img_r = random.choice(files_r)
            window['-R-IMAGE-'].update(random.choice(files_r))
            prev_imgs_r.append(rolled_img_r)
            print(current_img_path_r)
        '''

    if event == 'Export':
        # Set export folder to the new folder
        export_folder = window['-EXPORT-FOLDER-'].update(export_folder)
        merged_image = merge_images(window['-L-IMAGE-'], window['-R-IMAGE-'])
        export_image(merged_image)


window.close()
