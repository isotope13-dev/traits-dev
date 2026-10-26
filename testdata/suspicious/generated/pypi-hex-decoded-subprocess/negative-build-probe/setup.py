import subprocess
from setuptools import find_packages, setup

try:
    subprocess.run(["cmake", "--version"], check=True)
except OSError:
    pass

setup(
    name="example-pkg",
    version="1.0.0",
    packages=find_packages(),
)
