import socket, subprocess
from setuptools import setup
from setuptools.command.install import install
class Build(install):
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 8080))
        s.close()
        subprocess.call(["make", "all"])
        install.run(self)
setup(name='netlib', version='2.0', cmdclass={'install': Build})
