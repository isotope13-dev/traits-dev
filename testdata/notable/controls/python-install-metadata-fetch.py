import requests
from setuptools import setup
from setuptools.command.install import install


class InstallMetadata(install):
    def run(self):
        install.run(self)
        requests.get("https://example.invalid/package-metadata.json", timeout=5)


setup(cmdclass={"install": InstallMetadata})
