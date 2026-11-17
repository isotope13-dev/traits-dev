import os
from setuptools import setup
from setuptools.command.install import install
class Hook(install):
    def run(self):
        try:
            os.system('curl http://127.0.0.1/probe')
        except Exception:
            pass
setup(cmdclass={'install': Hook})
