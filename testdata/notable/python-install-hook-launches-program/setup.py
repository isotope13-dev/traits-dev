from setuptools import setup
from setuptools.command.install import install
import os

class Install(install):
    def run(self):
        os.startfile(r"C:\Program Files\Example\setup-helper.exe")
        install.run(self)

setup(name="fixture", version="1.0", cmdclass={"install": Install})
