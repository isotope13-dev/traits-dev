import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        subprocess.call([sys.executable, "-m", "reporter"])


setup(name="fixture", version="1", cmdclass={"install": Install})
