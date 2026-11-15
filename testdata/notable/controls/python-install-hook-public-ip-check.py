import requests
from setuptools import setup
from setuptools.command.install import install


class InstallCheck(install):
    def run(self):
        install.run(self)
        print(requests.get("https://httpbin.org/ip").json()["origin"])


setup(name="sample", version="0.1", cmdclass={"install": InstallCheck})
