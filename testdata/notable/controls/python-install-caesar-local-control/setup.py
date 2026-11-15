from setuptools import setup
from setuptools.command.install import install


class LocalInstall(install):
    def run(self):
        super().run()


setup(name="local-install-fixture", version="0.1", cmdclass={"install": LocalInstall})
