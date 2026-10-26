import ctypes
kernel32 = ctypes.windll.kernel32
address = kernel32.VirtualAllocEx(process, None, length, 0x3000, 0x04)
kernel32.WriteProcessMemory(process, address, data, length, None)
