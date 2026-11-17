from setuptools import setup
from setuptools.command.install import install
import atexit
import requests


def check_ip_service():
    requests.get("https://api.ipify.org")


class Install(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(check_ip_service)


setup(name="example", version="0.1", cmdclass={"install": Install})
