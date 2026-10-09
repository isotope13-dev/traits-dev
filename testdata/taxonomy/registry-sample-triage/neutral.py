from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
h = hashes.SHA256()
k = HKDF(algorithm=h, length=32, salt=b"salt", info=b"info")
x = getattr(response, "status_code", 200)
x = data.get("code")
m = {"idle":1,"time":2,"click":3,"count":4}
