import urllib.request
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        req = urllib.request.Request(
            "https://updates.example.invalid/status",
            data=b"version=1.0",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        urllib.request.urlopen(req)


setup(name="fixture", cmdclass={"install": Install})
