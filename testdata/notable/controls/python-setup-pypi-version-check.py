from setuptools import setup
from setuptools.command.install import install
from urllib import request


class CheckRelease(install):
    def run(self):
        with request.urlopen("https://pypi.org/pypi/example/json") as response:
            release_metadata = response.read()
        install.run(self)


setup(name="fixture", version="0.0.1", cmdclass={"install": CheckRelease})
