import json
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
payload = json.loads('{}')
encoded = json.dumps(payload)
raw = base64.b32decode('MZXW6===')
key = ed25519.Ed25519PrivateKey.from_private_bytes(raw)
if parts[1] in ('install', 'download', 'get'): pass
