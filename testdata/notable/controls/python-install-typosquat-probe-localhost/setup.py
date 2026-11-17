import urllib.request
from setuptools import setup
from setuptools.command.install import install
def report():
    result = urllib.request.urlopen('http://127.0.0.1/probe')
class Hook(install):
    def run(self):
        report()
setup(name='example', description='Security project to check how many developers install typoed libraries.', cmdclass={'install': Hook})
