import PySimpleGUI as sg

from create_new_block import create_new_window, run_create_new_window
from create_new_kette import create_kette_window, run_kette_window


def create_start_window() -> sg.Window:
    """
    Initial call function. This function should be called to create the start window.
    :return: the new start window.
    :rtype: sg.Window
    """
    layout = [[sg.Button("Neues Block-Schema", key="NEU")], [sg.Button("Neues Ketten-Schema", key="KETTE")]]
    window = sg.Window("Bahnsystem erstellen", layout=layout, size=(200, 100))
    return window


def run_start_window(window: sg.Window):
    event, value = window.read()
    if event == "NEU":
        window.close()
        new_window = create_new_window()
        run = run_create_new_window
    elif event == "KETTE":
        window.close()
        new_window = create_kette_window()
        run = run_kette_window
    else:
        return
    run(new_window)
