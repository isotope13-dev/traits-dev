from pathlib import Path
from PIL import ImageGrab

def save_snapshot(folder):
    target = Path(folder) / 'screenshot.png'
    ImageGrab.grab().save(target)
    return target

if __name__ == '__main__':
    save_snapshot('.')
