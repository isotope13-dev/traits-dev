import ctypes

def copy_bytes(dst, src, length):
    ctypes.memmove(dst, src, length)
