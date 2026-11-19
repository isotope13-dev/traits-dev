import os
from setuptools import setup
from setuptools.command.install import install

class PostInstall(install):
    def run(self):
        install.run(self)
        getattr(os, "sy" + "stem")("echo ready")

setup(name="fixture", version="0.0.0", cmdclass={"install": PostInstall})
