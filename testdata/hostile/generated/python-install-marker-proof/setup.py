import os, getpass
from setuptools import setup
from setuptools.command.install import install
class Hook(install):
    def run(self):
        path = os.path.join(os.path.expanduser('~'), 'marker')
        with open(path, 'a') as f:
            f.write(getpass.getuser())
setup(description='Code execution via Python package installation', cmdclass={'install': Hook})
