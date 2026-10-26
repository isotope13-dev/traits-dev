from setuptools import setup
import base64
import socket
import subprocess
from os import system

setup(name="sample-package", version="0.1")
payload = base64.b64decode("MSArIDE=")
system("python -c " + repr(payload.decode()))
subprocess.run(["python", "-c", payload.decode()])
eval(payload.decode())
configuration = {"script": payload.decode()}
eval(configuration["script"])
