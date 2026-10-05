import base64
import hashlib
import hmac
import json

# Documentation examples must not establish executed PRNG state recovery:
# s1 ^= s1 << 23
# s1 ^= LShR(s1, 17)
# s1 ^= LShR(s0, 26)
# solver.add(LShR(state0, 12) == int(output * (1 << 52)))
# session = {'username': 'admin', 'allow_session_ip_change': True}
def issue_cookie(secure_key, username):
    session = {'username': username}
    payload = base64.b64encode(json.dumps(session).encode()).decode()
    signature = hmac.new(secure_key, payload.encode(), hashlib.sha256).hexdigest()
    return 'session=' + payload + '; session.sig=' + signature
