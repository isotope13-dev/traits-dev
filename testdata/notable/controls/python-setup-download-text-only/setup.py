from setuptools import setup
import requests

readme = requests.get('https://example.invalid/README.md').text
open('README.md', 'w', encoding='utf-8').write(readme)

setup(name='setup-download-text-only-fixture', version='1.0')
