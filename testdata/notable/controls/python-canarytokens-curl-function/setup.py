import os
from setuptools import setup

def check():
    os.system("curl https://canarytokens.com/images/static/example/contact.php")

setup(name="example")
