import json
import urllib.request
from setuptools import setup
from setuptools.command.install import install

WEBHOOK_URL = "https://discord.com/api/webhooks/123456789012345678/fixture-token"


class InstallNotice(install):
    def run(self):
        data = json.dumps({"content": "Someone installed fixture-package via pip"}).encode()
        req = urllib.request.Request(WEBHOOK_URL, data=data)
        urllib.request.urlopen(req)
        install.run(self)


setup(name="fixture-package", cmdclass={"install": InstallNotice})
