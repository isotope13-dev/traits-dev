"""Independent PRNG simulation and ordinary server-side cookie signing."""
import base64
import hashlib
import hmac
import json

def step(older, newer):
    value = older
    value ^= (value << 23) & ((1 << 64) - 1)
    value ^= value >> 17
    return value ^ newer ^ (newer >> 26)

def sign_authenticated_admin(secret, now):
    session = {"username": "admin", "ts": now}
    payload = base64.b64encode(json.dumps(session).encode()).decode()
    signature = hmac.new(secret, payload.encode(), hashlib.sha1).hexdigest()
    return f"hfs_http={payload}; hfs_http.sig={signature}"

LOGIN_STAGE = "loginSrp1"
