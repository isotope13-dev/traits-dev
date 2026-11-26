import base64
import ctypes
import tkinter as tk
from io import BytesIO

import requests
from PIL import ImageGrab

API_URL = 'https://example.invalid/api'
session = requests.Session()


class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.after(5000, self.capture)

    def capture(self):
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
        shot = ImageGrab.grab()
        buf = BytesIO()
        shot.save(buf, format='JPEG')
        img = base64.b64encode(buf.getvalue()).decode('utf-8')
        session.post(API_URL, json={'image': img}, timeout=30)
        self.root.after(5000, self.capture)
