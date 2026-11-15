import subprocess
from setuptools import setup
from setuptools.command.install import install


class ShowBuildInfo(install):
    def run(self):
        install.run(self)
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Write-Output ready"],
            check=True,
        )


setup(name="fixture", version="0.0.1", cmdclass={"install": ShowBuildInfo})
