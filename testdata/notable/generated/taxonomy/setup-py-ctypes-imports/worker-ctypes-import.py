import ctypes

def load_library(name):
    return ctypes.CDLL(name)
