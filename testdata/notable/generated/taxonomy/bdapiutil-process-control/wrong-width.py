import ctypes
import subprocess
from ctypes import wintypes

def terminate_pid(pid):
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateFileW.restype = wintypes.HANDLE
    device = kernel.CreateFileW(r'\\.\BdApiUtil', 0xC0000000, 0, None, 3, 0, None)
    process_id = wintypes.DWORD(pid)
    returned = wintypes.DWORD()
    kernel.DeviceIoControl(device, 0x800024B4, ctypes.byref(process_id), 8, None, 0, ctypes.byref(returned), None)
    kernel.CloseHandle(device)

