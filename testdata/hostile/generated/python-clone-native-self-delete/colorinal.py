import ctypes
import os


def load_terminal_helper():
    try:
        return ctypes.CDLL(os.path.dirname(__file__) + "/" + "terminate.so")
    finally:
        os.remove(__file__)
