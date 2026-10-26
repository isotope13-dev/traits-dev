import os, subprocess, zipfile
from urllib.request import urlretrieve
from setuptools import setup
from setuptools.command.build_ext import build_ext

class Repackage(build_ext):
    def run(self):
        loc = os.getenv("ACME_PRECOMPILED_WHEEL_LOCATION", "https://example.com/acme.whl")
        urlretrieve(loc, filename="acme.whl")
        with zipfile.ZipFile("acme.whl") as wheel:
            wheel.extractall(".")

setup(name="acme", cmdclass={"build_ext": Repackage})
