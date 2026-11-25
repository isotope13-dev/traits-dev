import ctypes

user32 = ctypes.windll.user32
VK_F9 = 0x78


def pause_requested() -> bool:
    return bool(user32.GetAsyncKeyState(VK_F9) & 0x8000)
