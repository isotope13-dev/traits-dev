import os
import random
from PyWallpaper import change_wallpaper

images = [f for f in os.listdir("wallpapers") if f.endswith(".jpg")]
change_wallpaper(os.path.join("wallpapers", random.choice(images)))
