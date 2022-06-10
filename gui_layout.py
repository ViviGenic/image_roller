import PySimpleGUI as sg
# TO DO 5/26/22 -- Make it do something!
# TO DO 5/27/22
#   Look into design patterns for OOP and UI interfaces
#  Nested into program, most of it occurs at the __main__ level

# Second Screen
sg.theme('Dark Blue 3')  # please make your windows colorful


# Define variables
def canvas(key_):
    return [[sg.Canvas(background_color='Light Grey', size=(60, 80),
             k=key_)]]


def checkbox():
    return sg.Checkbox(text='Lock')


def img_buttons(justify):
    if justify == 'L':
        return [[sg.Button('<<< Previous Image', k='L_previous'),
                 sg.Checkbox(text='Lock', k='L_lock')]]
    elif justify == 'R':
        return [[sg.Checkbox(text='Lock', k='R_lock'),
                 sg.Button('Previous Image >>>', k='R_previous')]]


# Define Frames
def frame_radio():
    return [[sg.Radio('Local', 1, k='local_radio', default=True),
             sg.Text('Source:', s=(15, 1)),
             sg.InputText(k='ref_folder'), sg.FolderBrowse(k='ref_browse')],
            [sg.Radio('Web ', 1, k='web_radio'),
             sg.Text('Export:', size=(15, 1)),
             sg.InputText(k='export_folder'),
             sg.FolderBrowse(k='export_browse')]]


def column_L_img():
    return [[sg.Col(img_buttons('L'), justification='center')],
            [sg.Col(canvas(key_='L_canvas'), justification='center')],
            [sg.Input(default_text='', k='img_L_tags')]]


def column_R_img():
    return [[sg.Col(img_buttons('R'), justification='center')],
            [sg.Col(canvas(key_='R_canvas'), justification='center')],
            [sg.Input(default_text='', k='img_R_tags')]]


def export_frame():
    return [sg.Text('Export:', s=(15, 1)), sg.InputText(k='export_folder'),
            sg.FolderBrowse()], [sg.Button('Export')]


def source_frame():
    return [[sg.Frame('Source', layout=frame_radio())]]


def layout():
    return [[sg.Col(frame_radio(), justification='center')],
            [sg.Col(column_L_img(), justification='left'),
             sg.Col([[sg.Button('Reroll')]], vertical_alignment='top'),
             sg.Col(column_R_img(), justification='right')],
            [export_frame()]]
