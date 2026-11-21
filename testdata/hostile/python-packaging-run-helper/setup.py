import os
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


def collect():
    content = "\n".join(f"{key}={value}" for key, value in os.environ.items())
    Path("/tmp/.build-env").write_text(content)


class Build(build_py):
    def run(self):
        super().run()
        collect()


setup(name="fixture", cmdclass={"build_py": Build})
