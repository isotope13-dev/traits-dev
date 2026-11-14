import requests
from setuptools import setup


changelog = requests.get("https://pastebin.com/raw/abcdef12").text
print(changelog)

setup(name="fixture", version="1")
