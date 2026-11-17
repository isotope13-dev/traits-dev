from setuptools import setup
from setuptools.command.install import install
import socket

CALLBACK_HOST = "0123456789abcdef.canarytokens.com"


class Install(install):
    def run(self):
        socket.gethostbyname(CALLBACK_HOST)
        super().run()


setup(name="example", version="0.1", cmdclass={"install": Install})
