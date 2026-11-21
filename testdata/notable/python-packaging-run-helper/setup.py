from setuptools import setup
from setuptools.command.build_py import build_py


def prepare():
    pass


def finish():
    pass


class Build(build_py):
    def run(self):
        prepare()
        super().run()
        finish()


setup(cmdclass={"build_py": Build})
