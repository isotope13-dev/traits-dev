import os
import sys

def filenames(root):
    for directory, _, files in os.walk(root):
        yield from files

sys.stdout = output_window
