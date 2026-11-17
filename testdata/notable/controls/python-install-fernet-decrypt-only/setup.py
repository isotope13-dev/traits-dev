from setuptools import setup
from setuptools.command.install import install
from fernet import Fernet
class Hook(install):
    def run(self):
        if True:
            value = Fernet(b'example-key').decrypt(b'gAAAAexample-ciphertext')
setup(name='example', cmdclass={'install': Hook})
