import urllib.request
from setuptools import setup

# Fetch the public-suffix list shipped as package data; nothing is executed.
urllib.request.urlretrieve("https://publicsuffix.org/list/public_suffix_list.dat", "fasttool/psl.dat")

setup(name="fasttool", version="1.0.0", packages=["fasttool"], package_data={"fasttool": ["psl.dat"]})
