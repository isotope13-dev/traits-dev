import os
from setuptools import setup
from setuptools.command.install import install


class InstallSummary(install):
    def run(self):
        install.run(self)
        print(f"Installing for {len(os.environ)} configured environment values")


setup(name="sample", version="0.1", cmdclass={"install": InstallSummary})
