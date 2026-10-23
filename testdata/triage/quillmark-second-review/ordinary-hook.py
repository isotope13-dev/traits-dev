from setuptools import setup
from setuptools.command.install import install
class Custom(install):
    def run(self):
        install.run(self)
        print("Build complete")
setup(name="fixture", version="0.0.1", cmdclass={"install": Custom})
