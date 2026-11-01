from setuptools import setup
from setuptools.command.install import install
class CustomInstall(install):
    def run(self):
        print('building')
setup(cmdclass={'install': CustomInstall})
