import requests
from setuptools import setup
from setuptools.command.install import install

class Installer(install):
    def run(self):
        response = requests.post(URL, json={"content": "installed"})
        install.run(self)

URL = "https://discord.com/api/webhooks/your_webhook_url_here"
setup(name="sample", version="1", cmdclass={"install": Installer})
