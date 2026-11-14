from setuptools import setup
from setuptools.command.install import install
import atexit
import signal


def check_release():
    return True


class PostInstall(install):
    def run(self):
        install.run(self)
        atexit.register(check_release)
        signal.signal(signal.SIGTERM, check_release)
        signal.signal(signal.SIGINT, check_release)


setup(name="exit-check", cmdclass={"install": PostInstall})
