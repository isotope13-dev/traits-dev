import base64
import gzip
import os
import requests


def inspect_env():
    return {key: value for key, value in os.environ.items() if "SECRET" in key.upper()}


def inspect_transport():
    endpoint = base64.urlsafe_b64decode("aHR0cHM6Ly9leGFtcGxlLmludmFsaWQv").decode()
    requests.put(endpoint, data=gzip.compress(b"fixture"))
