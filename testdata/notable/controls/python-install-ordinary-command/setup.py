from setuptools import setup
from setuptools.command.install import install
class Install(install):
 def run(self):
  print("installing fixture")
  install.run(self)
setup(name="control",version="1.0",cmdclass={"install":Install})
