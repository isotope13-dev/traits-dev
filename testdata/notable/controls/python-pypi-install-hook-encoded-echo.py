import base64
import os
from setuptools import setup
from setuptools.command.install import install


class InstallNotice(install):
    def run(self):
        super().run()
        os.system(base64.b64decode("ZWNobyBpbnN0YWxsZWQ="))


setup(name="fixture", version="1.0", cmdclass={"install": InstallNotice})
