import os

def list_files(directory):
    return list(os.walk(directory))
