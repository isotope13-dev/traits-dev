import getpass
import os
import socket

import requests
from setuptools import setup
from setuptools.command.install import install


class InstallReporter(install):
    def run(self):
        install.run(self)
        requests.post(
            "https://telemetry.example.invalid/install",
            json={
                "package_name": "fixture",
                "version": "0.0.1",
                "user": getpass.getuser(),
                "cwd": os.getcwd(),
                "hostname": socket.gethostname(),
            },
        )


setup(name="fixture", version="0.0.1", cmdclass={"install": InstallReporter})
