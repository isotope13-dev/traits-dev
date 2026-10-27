import base64
raw = base64.b64decode("dGVzdA==")
print(raw.decode())
