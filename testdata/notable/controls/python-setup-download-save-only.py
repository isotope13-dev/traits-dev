import requests
from setuptools import setup


class FetchDocumentation:
    def run(self):
        response = requests.get("https://example.org/release-notes.txt")
        with open("release-notes.txt", "wb") as output:
            output.write(response.content)


setup(name="fixture", version="0.0.1", cmdclass={"install": FetchDocumentation})
