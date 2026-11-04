from setuptools import setup
from setuptools.command.install import install
import requests

class InstallCommand(install):
    def run(self):
        response = requests.get('https://example.invalid/version').text
        print(response)
        exec(compile('print("local build")', '<local>', 'exec'), {})
        install.run(self)

setup(name='build-example', version='1.0', cmdclass={'install': InstallCommand})
