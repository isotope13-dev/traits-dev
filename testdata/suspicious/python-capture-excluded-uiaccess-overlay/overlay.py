import ctypes
user32 = ctypes.windll.user32
advapi32 = ctypes.windll.advapi32
WDA_EXCLUDEFROMCAPTURE = 0x11
fn = kernel32.GetProcAddress(h_user32, b"CreateWindowInBand")
advapi32.DuplicateTokenEx(tok, 0x2000000, None, 2, 1, ctypes.byref(new_tok))
hwnd = p_create(0x8, atom, None, 0x90000000, 0, 0, w, h, None, None, None, None, 2)
user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
