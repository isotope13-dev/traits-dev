import os
from setuptools import setup
from setuptools.command.install import install
class X(install):
    def run(self):
        install.run(self)
        # os.system('pip3 uninstall foo -y')
        os.system('ldconfig')
setup(name='foo', version='9007.0.1', cmdclass={'install': X})
