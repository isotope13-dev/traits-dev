from setuptools import setup
from urllib.request import urlretrieve

# A download alone does not prove activation of the downloaded file.
urlretrieve('https://downloads.example.invalid/vendor.exe', 'vendor.exe')
setup(name='vendor-assets', version='1.0')
