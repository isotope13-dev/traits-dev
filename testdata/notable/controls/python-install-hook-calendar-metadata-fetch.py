import os
from pathlib import Path

import requests
from setuptools import setup
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        super().run()
        config_dir = Path.home() / ".config" / "calendar"
        config_dir.mkdir(parents=True, exist_ok=True)
        response = requests.get("https://updates.example.org/calendar.json")
        if response.ok:
            (config_dir / "calendar.json").write_text(response.text)


setup(name="calendar-fixture", version="0.1", cmdclass={"install": InstallCommand})
