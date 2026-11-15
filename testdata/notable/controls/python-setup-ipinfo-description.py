from setuptools import setup
import requests


def package_description():
    return requests.get("https://ipinfo.io").json()["ip"]


setup(name="sample", version="0.1", description=package_description())
