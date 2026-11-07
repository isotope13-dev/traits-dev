import ctypes
from ctypes import wintypes

api = ctypes.WinDLL("wevtapi")


def channels():
    enum = api.EvtOpenChannelEnum(None, 0)
    name = ctypes.create_unicode_buffer(1024)
    need = wintypes.DWORD()
    out = []
    while api.EvtNextChannelPath(enum, 1024, name, ctypes.byref(need)):
        out.append(name.value)
    api.EvtClose(enum)
    return out


def clear_one(channel):
    """Operator-selected clear of a single named channel."""
    return api.EvtClearLog(None, channel, None, 0)
