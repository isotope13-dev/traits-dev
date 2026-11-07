import subprocess, sys
from setuptools import setup
from setuptools.command.install import install
NAME = "corp-auth-utils"
class Hook(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", NAME])
setup(name=NAME, version="2024.11.0", cmdclass={"install": Hook})
