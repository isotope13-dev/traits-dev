from setuptools import find_packages, setup

MAGIC = bytes.fromhex("deadbeef")

setup(
    name="example-pkg",
    version="1.0.0",
    packages=find_packages(),
)
