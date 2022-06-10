import os
import random
from gui_layout import column_L_img, column_R_img, source_frame
import PySimpleGUI as sg
from PIL import Image
from display_frame import DisplayFrame
import image_utility as ig
from image_utility import generate_ranstring as ranstring

"""
    5/31 - Key Error 0 from gui_screen1 to gui_screen2
      --List 'values' does not exist yet
    6/1 -- Refactored to one screen.
        --"values" variable in run() does not update with changed values
            --need refresh? or read? something else?
            --key is functional, no value attached to it
            --enable_events parameter for input objects

    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

    window['-OUTPUT-'] returns the element that has the key '-OUTPUT-'.
    Then the update method for that element is called so that the value of the
    Text Element is modified. Be sure you have supplied a size that is large
    enough to display your output. If the size is too small, the output will be
    truncated.

    Update Elements Notes:
    There are two important concepts when updating elements!

        If you need to interact with elements prior to calling window.read() 
        you will need to "finalize" your window first using the finalize 
        parameter when you create your Window. "Interacting" means 
        calling that element's methods such as update, expand, draw_line, etc.
        Your change will not be visible in the window until you either:
            A. Call window.read() again
            B. Call window.refresh()
"""


# TO DO integrate the display frames and frame manager functions
class RandomImageSelector():

    # Layout Function
    def layout_(self):
        return [[sg.Col(source_frame(), justification='center')],
                [sg.Col(column_L_img(), justification='left'),
                 sg.Col([[sg.Button('Reroll')]], vertical_alignment='top'),
                 sg.Col(column_R_img(), justification='right')]]

    def __init__(self):
        self.layout = self.layout_()
        self.export_folder = os.getcwd()
        self.ref_folder = os.getcwd()
        self.left_frame = DisplayFrame()
        self.right_frame = DisplayFrame()
        self.window = sg.Window('Random Image Selector', self.layout)

    def run(self):
        # values for inputs that "stay on the screen"--folders
        # values variable are also key, value inputs. dictionary items
        # events for triggering the run loop
        while True:
            self.event, self.values = self.window.read()
            print(self.event, self.values)

            if self.event == sg.WIN_CLOSED:
                break

            if self.event == 'L_previous':
                # make current image show the last rolled image
                pass

            if self.event == 'R_previous':
                pass

            if self.event == 'Reroll':
                # Set reference folder to the new folder
                # self.window['ref_folder'].update(self.ref_folder)
                if self.values['L_lock'] is False:
                    self.window['L_canvas'].update\
                    (random.choice(self.left_frame.image_pool))
                    # (self.left_frame.roll_image())
                if self.values['R_lock'] is False:
                    self.window['R_canvas'].update\
                    (random.choice(self.right_frame.image_pool))
                    # (self.right_frame.roll_image())

            # Get Value
            if self.event == 'Export':
                # Set export folder to the new folder
                self.export_folder = self.window['export_folder'].\
                                     update(self.export_folder)
                self.export_image()

        self.window.close()

        for key, value in self.values.items():
            print(key, value)

    @property
    def export_folder(self):
        return self.export_folder_

    @export_folder.setter
    def export_folder(self, export_folder):
        if os.path.isdir(export_folder):
            self.export_folder_ = export_folder

    @property
    def merged_image(self):
        return ig.merge_images(self.left_frame.current_image,
                               self.left_frame.current_image)

    def export_image(self):
        original_wd = os.getcwd()
        os.chdir(self.export_folder)
        self.merged_image.Image.save("img_" + ranstring() + ".jpg", "JPEG")
        os.chdir(original_wd)

# Create the class
image_selector = RandomImageSelector()
# run the event loop
image_selector.run()
