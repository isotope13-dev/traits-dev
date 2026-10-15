"""Static near miss: imports ctypes and mmap but only requests RW memory."""
import ctypes
import mmap


def reserve_data_region(size):
    return mmap.mmap(-1, size, prot=mmap.PROT_READ | mmap.PROT_WRITE)
