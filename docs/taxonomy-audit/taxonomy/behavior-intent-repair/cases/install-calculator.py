import os
from setuptools import setup
from setuptools.command.install import install
class CustomInstall(install):
    def run(self):
        os.system('calc.exe')
setup(cmdclass={'install': CustomInstall})
