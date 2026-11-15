from setuptools import setup
from setuptools.command.install import install


class InstallInfo(install):
    def run(self):
        from local_info import show
        show()
        install.run(self)


setup(name="local-info-fixture", version="0.1", cmdclass={"install": InstallInfo})
