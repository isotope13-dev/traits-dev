import os
import shutil
import subprocess

from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py


class NativeBuildExt(build_ext):
    def run(self):
        if shutil.which("cargo"):
            subprocess.run(
                ["cargo", "build", "--release"],
                check=True,
            )
        super().run()


class NativeBuildPy(build_py):
    def run(self):
        super().run()


setup(
    name="example-native-pkg",
    version="0.1",
    cmdclass={"build_ext": NativeBuildExt, "build_py": NativeBuildPy},
)


def _missing_helper_message():
    # Help text for users without the optional build backend. This is a
    # message, not an install command: it must never read as a dropper.
    print("Install maturin to enable: pip install maturin")
