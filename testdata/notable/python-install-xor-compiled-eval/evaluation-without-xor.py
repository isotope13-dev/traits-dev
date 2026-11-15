from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        eval(compile("print('visible source')", "<string>", "exec"))
        install.run(self)


setup(name="sample", cmdclass={"install": CustomInstallCommand})
