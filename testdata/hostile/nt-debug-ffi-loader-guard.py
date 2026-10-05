import ctypes
from ctypes import wintypes

ntdll = ctypes.WinDLL("ntdll.dll")
ntdll.NtQueryInformationProcess.argtypes = [wintypes.HANDLE, wintypes.ULONG,
    ctypes.c_void_p, wintypes.ULONG, ctypes.c_void_p]
ntdll.NtQueryInformationProcess.restype = wintypes.LONG
ntdll.NtSetInformationThread.argtypes = [wintypes.HANDLE, wintypes.ULONG,
    ctypes.c_void_p, wintypes.ULONG]
ntdll.NtSetInformationThread.restype = wintypes.LONG

def prepare_loader():
    flags = wintypes.ULONG()
    status = ntdll.NtQueryInformationProcess(-1, 0x1f, ctypes.byref(flags),
                                            ctypes.sizeof(flags), None)
    if status < 0 or not flags.value:
        return False
    return ntdll.NtSetInformationThread(-2, 0x11, None, 0) >= 0
