from setuptools import setup
import subprocess
import sys

def install():
    suffix = bytes.fromhex('646973745f696e666f').decode()
    if 'install' in sys.argv:
        subprocess.run(['mspaint'])
    return suffix

setup(name='image-helper', version='1.0.0')
