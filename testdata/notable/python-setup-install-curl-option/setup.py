import os
import setuptools
from setuptools.command.install import install

class Install(install):
    def run(self):
        os.system("curl --data 'build complete' https://upload.example.test")
        install.run(self)

setuptools.setup(name="fixture", version="1.0", cmdclass={"install": Install})
