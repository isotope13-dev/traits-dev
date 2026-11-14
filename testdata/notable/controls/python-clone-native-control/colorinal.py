import ctypes
import os


def load_terminal_helper():
    return ctypes.CDLL(os.path.dirname(__file__) + "/" + "terminal.so")
