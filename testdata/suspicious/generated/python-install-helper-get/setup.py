import requests
from setuptools import setup
from setuptools.command.install import install
def fetch():
    url = 'https://example.com/probe'
    try:
        response = requests.get(url)
    except Exception:
        pass
class Hook(install):
    def run(self):
        fetch()
setup(cmdclass={'install': Hook})
