from setuptools import setup
from setuptools.command.egg_info import egg_info
class Metadata(egg_info):
 def run(self):
  print("building metadata")
  egg_info.run(self)
setup(name="metadata-control",version="1.0",cmdclass={"egg_info":Metadata})
