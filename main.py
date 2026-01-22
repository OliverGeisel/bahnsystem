#!/usr/bin/env python3
"""
Main entry point for the GUI application.
This module initializes and runs the starting window of the GUI, allowing users to choose between creating a new block schema or a new chain schema.
"""
import gui


def run():
    window = gui.create_start_window()
    gui.run_start_window(window)


if __name__ == '__main__':
    run()
