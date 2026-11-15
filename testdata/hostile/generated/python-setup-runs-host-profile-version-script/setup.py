import subprocess
import sys
from setuptools import setup


def read_version():
    ver = "fixture_package/version"
    subprocess.Popen([sys.executable, ver])
    return "1.0"


setup(name="ttensorflow-gpu", version=read_version())
