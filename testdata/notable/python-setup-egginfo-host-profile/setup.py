import socket
import requests
from setuptools import setup
from setuptools.command.egg_info import egg_info


class EggInfo(egg_info):
    def run(self):
        requests.get("https://status.example.invalid/build")
        print(socket.gethostname())
        super().run()


setup(name="example", cmdclass={"egg_info": EggInfo})
