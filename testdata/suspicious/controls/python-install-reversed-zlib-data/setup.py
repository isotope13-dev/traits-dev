import base64
import zlib
from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def run(self):
        decode = lambda value: __import__('zlib').decompress(__import__('base64').b64decode(value[::-1]))
        print((decode)(b'==AsCUhDAQA1wE9KMrMKrwJe'))
        install.run(self)

setup(name='example', cmdclass={'install': Install})
