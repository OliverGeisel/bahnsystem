"""
This module contains the GUI for creating new block or chain schemas. It uses PySimpleGUI4 to create the windows and handle user interactions.
This is the starting point of the GUI, allowing users to choose between creating a new block schema or a new chain schema.
"""
import PySimpleGUI4 as sg

from create_new_block import create_new_block_window, run_create_new_window
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
    """
    Starting point of the GUI. This function runs the start window and handles the navigation to other windows.
    :param window:  The start window to run.
    :type window: sg.Window
    :return: None
    """
    event, value = window.read()
    if event == "NEU":
        window.close()
        new_window = create_new_block_window()
        run = run_create_new_window
    elif event == "KETTE":
        window.close()
        new_window = create_kette_window()
        run = run_kette_window
    else:
        return
    run(new_window)
