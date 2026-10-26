# Static near miss: a native build reports constant build status. The database
# setting gates optional features; its value is never harvested or uploaded.
import os
import subprocess
import urllib.request
import setuptools
import setuptools.command.install

class Build(setuptools.command.install.install):
    def run(self):
        if os.environ.get("DATABASE_URL"):
            print("database support enabled")
        request = urllib.request.Request("http://1.1.1.1:8080/status", data=b"build_started")
        urllib.request.urlopen(request)
        subprocess.run(["cc", "-c", "extension.c"], check=True)
        setuptools.command.install.install.run(self)

setuptools.setup(name="native-status-control", cmdclass={"install": Build})
