from setuptools import setup
import base64
import socket

setup(name="sample-package", version="0.1")
encoded = base64.b64encode(b"package data")
print(encoded)
