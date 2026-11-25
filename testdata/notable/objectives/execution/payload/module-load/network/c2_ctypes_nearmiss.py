import base64
import ctypes
import urllib.request

def load_system_libc():
    return ctypes.CDLL("libc.so.6")




























































def fetch_and_decode(url):
    req = urllib.request.Request(url)
    return base64.b64decode(b"aGVsbG8=")

def save_report(path, text):
    with open(path, "w") as fh:
        fh.write(text)
