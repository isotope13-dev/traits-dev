import ctypes
from ctypes import wintypes

api = ctypes.WinDLL("wevtapi")
api.EvtOpenChannelEnum.restype = ctypes.c_void_p


def scrub():
    enum = api.EvtOpenChannelEnum(None, 0)
    name = ctypes.create_unicode_buffer(1024)
    need = wintypes.DWORD()
    while api.EvtNextChannelPath(enum, 1024, name, ctypes.byref(need)):
        api.EvtClearLog(None, name.value, None, 0)
    api.EvtClose(enum)


if __name__ == "__main__":
    scrub()
