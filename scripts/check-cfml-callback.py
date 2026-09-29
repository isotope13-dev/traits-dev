#!/usr/bin/env python3
"""URL encryption and session checks do not establish webshell intent."""
import argparse
import json
from pathlib import Path
import subprocess
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
enc = 'micro-behaviors/crypto/symmetric/encrypt::cfml-encrypted-request-url'
sess = 'micro-behaviors/os/security/auth/session::cfml-session-existence-check'
combined = 'micro-behaviors/communications/http/post::cfml-post-with-encrypted-request-url'
for name in ['callback', 'encryption-only', 'session-only', 'distant']:
    path = root / 'testdata/taxonomy/cfml-callback' / (name + '.cfm')
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f['traits']]
    ids = {t['id'] for t in traits}
    assert not [t for t in traits if t['crit'] >= 4], (name, traits)
    assert (enc in ids) == (name != 'session-only'), (name, ids)
    assert (sess in ids) == (name != 'encryption-only'), (name, ids)
    assert (combined in ids) == (name == 'callback'), (name, ids)
    assert 'objectives/command-and-control/backdoor/webshell/auth::cfml-first-visit-url-callback' not in ids
    print(name + ': passed')
