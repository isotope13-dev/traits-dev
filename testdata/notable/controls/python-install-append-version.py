from pathlib import Path
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        Path("installed-version.txt").write_text("1.0\n", encoding="utf-8")


setup(name="fixture", cmdclass={"install": Install})
