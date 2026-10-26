from setuptools import setup
from setuptools.command.install import install
import subprocess


class CustomInstall(install):
    def run(self):
        subprocess.call("pip install example-dep --quiet", shell=True)
        install.run(self)


setup(name="example-pkg", version="0.1", cmdclass={"install": CustomInstall})
