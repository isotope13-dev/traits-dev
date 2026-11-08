import urllib.request, subprocess
from setuptools import setup
urllib.request.urlretrieve("https://example.org/README.html", "docs.html")
subprocess.run(["start", "index.html"], shell=True)
setup(name="c2", version="1.0")
