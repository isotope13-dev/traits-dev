# Static detection fixture. Never execute: this sketches the DirtyCow
# (CVE-2016-5195) primitive pair -- the nickname beside a live-memory write
# -- so the name-plus-behavior composite keeps convicting while bare
# nickname maps stay reference-level.
#
# Guards: dirtycow-detected must fire suspicious when the DirtyCow name or
# CVE-2016-5195 appears beside a /proc/self/mem write.
import ctypes
import os

# DirtyCow CVE-2016-5195 proof of concept sketch: race madvise against a
# write to the read-only mapping via /proc/self/mem.
LIBC = ctypes.CDLL("libc.so.6", use_errno=True)


def dirtycow_write(path, offset, payload):
    f = os.open(path, os.O_RDONLY)
    mapping = LIBC.mmap(0, 4096, 1, 2, f, 0)
    mem = os.open("/proc/self/mem", os.O_RDWR)
    os.lseek(mem, mapping + offset, os.SEEK_SET)
    os.write(mem, payload)
    os.close(mem)
    os.close(f)
