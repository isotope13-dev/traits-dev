import requests
from setuptools import setup
from setuptools.command.install import install

class Installer(install):
    def run(self):
        requests.post(URL, json={"content": "installed"})
        install.run(self)

URL = "https://discord.com/api/webhooks/123456789012345678/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi1234567890"
setup(name="sample", version="1", cmdclass={})
