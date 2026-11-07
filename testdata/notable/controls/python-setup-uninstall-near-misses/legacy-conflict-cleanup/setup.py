import os
from setuptools import setup
from setuptools.command.install import install
class Cleanup(install):
    """Remove the legacy distribution that conflicts with this one."""
    def run(self):
        os.system('pip uninstall -y opencv-python-legacy')
        install.run(self)
setup(name='opencv-contrib-fork', version='4.8.1', cmdclass={'install': Cleanup})
