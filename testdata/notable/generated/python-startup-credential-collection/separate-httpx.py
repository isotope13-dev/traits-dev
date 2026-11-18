import base64
import httpx
import os


def inspect_env():
    return {key: value for key, value in os.environ.items() if "TOKEN" in key.upper()}


def inspect_transport():
    target = base64.b64decode("aHR0cHM6Ly9leGFtcGxlLmludmFsaWQv").decode()
    httpx.post(target, content=b"fixture")
    httpx.post("https://example.invalid/", content=base64.b64encode(b"fixture"))
