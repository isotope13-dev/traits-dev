"""Return example Telegram data locations without reading their contents."""
import os


def example_locations(root):
    return [
        "/Users/example/Library/Application Support/Telegram Desktop/tdata/",
        r"C:\Users\example\AppData\Roaming\Telegram Desktop\tdata",
        os.path.join(root, "Telegram Desktop", "tdata"),
        os.path.join(root, "Telegram", "tdata"),
        "/example/Telegram/tdata/",
    ]
