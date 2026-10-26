import ctypes
ntdll = ctypes.windll.ntdll
ntdll.RtlAdjustPrivilege(20, True, False, ctypes.byref(ctypes.c_bool()))
