"""Near miss: install hook checks a normal package health endpoint."""

from setuptools import setup
from setuptools.command.install import install
import requests


class CustomInstall(install):
    def run(self):
        requests.get("https://pypi.org/pypi/example/json")


setup(name="example-package", cmdclass={"install": CustomInstall})
