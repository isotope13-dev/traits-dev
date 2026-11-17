import urllib.request
from setuptools import setup
from setuptools.command.install import install

def ping():
    reply = urllib.request.urlopen("https://127.0.0.1/check")

class PostInstall(install):
    def run(self):
        ping()
        install.run(self)

setup(name="probe", version="1", description="Security project for PoC", packages=[], cmdclass={"install": PostInstall})
