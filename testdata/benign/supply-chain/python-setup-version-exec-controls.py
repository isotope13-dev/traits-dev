"""Packaging shape: custom build_ext plus local version-file exec.

Mirrors pyzmq's setup.py: a cmdclass build_ext hook lives near an
extract_version() helper that execs lines read from the package's own
version.py, so the version is learned without importing the package.
The exec input is locally-read source, not an install-time payload.
"""
import os
from distutils.command.build_ext import build_ext
from distutils.core import setup


class CheckingBuildExt(build_ext):
    def run(self):
        build_ext.run(self)


def extract_version():
    """Read the version without importing the package."""
    with open(os.path.join("zmq", "sugar", "version.py")) as f:
        lines = f.readlines()
    ns = {}
    exec(''.join(lines), ns)
    return ns["__version__"]


cmdclass = {"build_ext": CheckingBuildExt}

setup(
    name="example-native",
    version=extract_version(),
    cmdclass=cmdclass,
)
