import ctypes
import os

# Benign helper-library control mirroring the overturned sample's shape:
# embedded bytes materialized from a module attribute, written to APPDATA,
# and loaded for in-process calls. No transfer-of-execution primitive, so
# the tightened hostile must stay silent (only neutral micro-behaviors).
from res import bin


def load_helper():
    try:
        with open("%s\\scanhelp.dll" % os.getenv("APPDATA"), "wb") as file:
            file.write(bytes(res.bin))
    except OSError:
        pass
    return ctypes.WinDLL(os.getenv("APPDATA") + "\\scanhelp.dll")
