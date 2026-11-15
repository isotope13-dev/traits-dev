from setuptools import setup
from setuptools.command.egg_info import egg_info


class MetadataCommand(egg_info):
    def run(self):
        egg_info.run(self)


setup(name="sample", version="0.0.1", cmdclass={"egg_info": MetadataCommand})
