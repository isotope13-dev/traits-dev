import base64
raw = base64.b64decode("CzZ7eQ==")
result = bytes([c ^ 90 for c in raw]).decode()
print(result)
