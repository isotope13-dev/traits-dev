"""Static near miss: executable mmap syntax without a ctypes import."""
import mmap


def reserve_executable_region(size):
    return mmap.mmap(-1, size, prot=mmap.PROT_READ | mmap.PROT_EXEC)
