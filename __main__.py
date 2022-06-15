import os
import io
import random
import PySimpleGUI as sg
import PIL.Image
import glob as gl
import string


ref_folder_l = r'.'
ref_folder_r = r'.'
export_folder = r'.'


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


def merge_images(image1, image2):
    # Compare and resize image to match small of the 2
    # find small, reduce large image to it's size --
    # do this in *one* line of code
    # get height, width of image
    large_img, small_img = compare_image_sizes(image1, image2)
    large_img = large_img.resize((small_img.height, small_img.width))
    new_image = PIL.Image.new('RGB', (2*small_img.size[0], small_img.size[1]),
                                 (250, 250, 250))
    new_image.paste(small_img, (0, 0))
    new_image.paste(large_img, (small_img.size[0], 0))
    return new_image


def export_image(merged_image):
    merged_image.PIL.Image.save(export_folder + "img_" + generate_ranstring() + ".jpg", "JPEG")


# Needs to have a working directory confirmed
def list_images():
    files = gl.glob('*.png') + gl.glob('*.gif') + gl.glob('*.jpg')
    return files


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = PIL.Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def convert_to_bytes(file_or_bytes, resize=None, fill=False):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :param fill: If True then the image is filled/padded so that the image is not distorted
    :type fill: (bool)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    if fill:
        if resize is not None:
            img = make_square(img, resize[0])
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


# Layout Generator Functions
def img_buttons(justify):
    if justify == 'L':
        return [[sg.Button('<<< Previous Image', k='-L-PREVIOUS-'),
                 sg.Checkbox(text='Lock', k='-L-LOCK-')]]
    elif justify == 'R':
        return [[sg.Checkbox(text='Lock', k='-R-LOCK-'),
                 sg.Button('Previous Image >>>', k='-R-PREVIOUS-')]]

# TO DO -- Break Reference Folders into 2, -L-REF-FOLDER- and -R-REF-FOLDER-
def source_column():
    return [[sg.Radio('Local', 1, k='-LOCAL-RADIO-', default=True),
             sg.Text('Left Source:'),
             sg.InputText(k='L-REF-FOLDER-'), sg.FolderBrowse(k='L-REF-BROWSE-')],
            [sg.Radio('Web ', 1, k='-WEB-RADIO'),
             sg.Text('Export:', size=(15, 1)),
             sg.InputText(k='-EXPORT-FOLDER-'),
             sg.FolderBrowse(k='-EXPORT-BROWSE')]]


def image_element(side):
    return [[sg.Image(k = '-' + side + '-IMAGE-',
            background_color = 'Light Grey', size=(60, 80))]]


# TO DO -- Add Individual Ref Folders and Thumbnails of Previous Images
def column_img(side):
    return [[sg.Column(img_buttons(side), justification='center')],
            [sg.Column(image_element(side), justification='center')],
            [sg.Input(default_text='', k = '-' + side + '-IMG-TAGS')]]


def reroll_button():
    return [[sg.Button('Reroll')]]


def export_column():
    return [[sg.Text('Export:'), sg.InputText(k='-EXPORT-FOLDER-'),
            sg.FolderBrowse(), sg.Button('Export')]]


layout = [
            [sg.Column(source_column(), justification='center')],
            [sg.Column(column_img('L'), justification='left'), sg.Column(column_img('R'), justification='right')],
            [sg.Column(export_column(), justification='center')]
        ]


for element in layout:
    print(element)
    print(type(element))
    if element is type(list):
        for subelement in element:
            print(subelement)
            print(type(subelement))

#sg.Column(reroll_button())

window = sg.Window('Random Image Selector', layout = layout)

files_l = [os.path.join(ref_folder_l, l) for l in os.listdir(ref_folder_l) if l.endswith('png')]
files_r = [os.path.join(ref_folder_r, r) for r in os.listdir(ref_folder_r) if r.endswith('png')]

previous_imgs_l = []
previous_imgs_r = []

# Event Loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-L-PREVIOUS-':
        # make current image show the last rolled image
        pass

    if event == '-R-PREVIOUS-':
        pass

    if event == 'Reroll':
        # Set reference folder to the new folder
        # window['ref_folder'].update(ref_folder)
        if values['-L-LOCK-'] is False:
            previous_imgs_l.append.window['-L-IMAGE-']      #append current image to previous images list
            window['-L-IMAGE-'].update(random.choice(files_l))
        if values['-R-LOCK-'] is False:
            previous_imgs_r.append.window['-R-IMAGE-']
            window['-R-IMAGE-'].update(random.choice(files_r))


    # Get Value
    if event == 'Export':
        # Set export folder to the new folder
        export_folder = window['-EXPORT-FOLDER-'].update(export_folder)
        merged_image = merge_images(values['-L-IMAGE-'], values['-R-IMAGE-'])
        export_image(merged_image)


window.close()


for key, value in values.items():
    print(key, value)







