from setuptools import setup
from setuptools.command.install import install
import os
class Installer(install):
    def run(self):
        os.system("calc.exe")
setup(name="fixture", version="1.0", cmdclass={"install": Installer})
