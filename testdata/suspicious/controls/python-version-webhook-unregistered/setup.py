import sys, requests
from setuptools import setup
from setuptools.command.install import install

class Hook(install):
    def run(self):
        url = 'https://webhook.site/abc'
        data = {'event': 'installation', 'python_version': sys.version}
        try:
            response = requests.post(url, json=data)
        except Exception:
            pass
setup(name='sample')

class Other(install):
    def run(self):
        pass
setup(name='other', cmdclass={'install': Other})
