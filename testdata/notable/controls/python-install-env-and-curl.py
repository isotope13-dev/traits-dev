import os
import subprocess
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        subprocess.check_output(["curl", "https://example.invalid/health"])
        for name, value in os.environ.items():
            print(name, bool(value))


setup(name="fixture", cmdclass={"install": Install})
