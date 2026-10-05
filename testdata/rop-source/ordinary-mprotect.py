import ctypes
libc = ctypes.CDLL(None)
libc.mprotect(0x100000, 4096, 7)
