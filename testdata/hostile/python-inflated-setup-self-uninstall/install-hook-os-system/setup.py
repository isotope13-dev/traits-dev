# Reduced from genz_translator 9007.0.1: live self-uninstall in an install
# hook under an inflated version; credentials and hosts replaced.
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install
import os
import sys

VERSION = 'v9007.0.1'
PACKAGE_NAME = "internal_translator"
INTERNAL_REPO_IP = "pkgs.example.invalid"
INTERNAL_REPO_URL = "http://reader:example-secret@pkgs.example.invalid:8010/simple/"


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        actual_path = ""
        for path in sys.path:
            if os.path.isdir(path + "/" + PACKAGE_NAME + "-" + VERSION.replace('v', '') + ".dist-info"):
                actual_path = path + "/"
                break
        os.system('pip3 --verbose uninstall ' + PACKAGE_NAME + ' -y')
        #os.system('pip3 install ' + PACKAGE_NAME + ' --trusted-host ' + INTERNAL_REPO_IP + ' --index-url "' + INTERNAL_REPO_URL + '"')


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    cmdclass={'install': PostInstallCommand},
)
