#!/usr/bin/env python3

import os, sys, subprocess
from pynput import keyboard
from pygments import formatters, highlight, lexers
from pygments.util import ClassNotFound
from simple_term_menu import TerminalMenu
from termcolor import colored

def highlight_file(filepath):
    try:
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                file_content = f.read()
            try:
                lexer = lexers.get_lexer_for_filename(filepath, stripnl=False, stripall=False)
            except ClassNotFound:
                lexer = lexers.get_lexer_by_name("text", stripnl=False, stripall=False)
            formatter = formatters.TerminalFormatter(bg="dark")  # dark or light
            highlighted_file_content = highlight(file_content, lexer, formatter)
            return highlighted_file_content
        elif os.path.isdir(filepath):
            items = os.listdir(filepath)
            if len(items) <= 0:
                return "No items in this directory."
            else:
                return '\n'.join(items)
    except PermissionError as e:
        return "Insufficient"
    except Exception as e:
        return "Error displaying file content."

def list_files(directory="."):
    items = [file for file in os.listdir(directory)]
    if len(items) < 1:
        items.insert(0,"NOTHING TO SEE HERE")
    else:
        items.insert(0,"BACK")
    return items

def main():
    while True:
        items = list_files()
        terminal_menu = TerminalMenu(items, preview_command=highlight_file, preview_size=0.75, title=f'Stupid Simple Directory Navigator\n{os.getcwd()}', clear_screen=True, quit_keys=("escape", "q"), accept_keys=("enter", "escape", "q", "l", "h"))
        try:
            menu_entry_index = terminal_menu.show()
            if(terminal_menu.chosen_accept_key == "escape" or terminal_menu.chosen_accept_key == "q"):
                print("Quitting...")
                break
            elif(terminal_menu.chosen_accept_key == "h"):
                os.chdir("..")
            else:
                selection = items[menu_entry_index]
                if os.path.isdir(selection):
                    os.chdir(selection)
                elif os.path.isfile(selection):
                    subprocess.run(["vi", selection])
                    sys.exit(0)
                elif selection == "NOTHING TO SEE HERE" or selection == "BACK":
                    os.chdir("..")
                else:
                    print("Weird error")
                    break
        except TypeError as e:
            continue

if __name__ == "__main__":
    main()
