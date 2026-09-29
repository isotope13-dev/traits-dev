#!/usr/bin/env python3
"""Datasource access and password decryption require hostile context."""
import argparse
import json
from pathlib import Path
import subprocess
p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
args = p.parse_args()
root = Path(__file__).resolve().parents[1]
objective = 'objectives/credential-access/theft/app::cfml-webshell-datasource-password-decryption'
for name in ['enumeration', 'decryption', 'credential-shell']:
    path = root / 'testdata/taxonomy/cfml-datasource' / (name + '.cfm')
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    ts = [t for f in json.loads(result.stdout)['files'] for t in f['traits']]
    ids = {t['id'] for t in ts}
    assert (objective in ids) == (name == 'credential-shell'), (name, ids)
    if name != 'credential-shell':
        assert not [t for t in ts if t['crit'] >= 4], (name, ts)
    if name in ['enumeration', 'credential-shell']:
        assert 'micro-behaviors/data/db/config::cfml-datasource-service-enumeration' in ids
    if name in ['decryption', 'credential-shell']:
        assert 'micro-behaviors/crypto/symmetric/decrypt::cfml-decrypt-password-member' in ids
    print(name + ': passed')
