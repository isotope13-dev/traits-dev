#!/usr/bin/env python3
"""CFML password/session observations must not classify login pages as shells."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
base = 'micro-behaviors/os/security/auth/verify::'
combined = base + 'cfml-password-literal-session-comparison'
obsolete = 'objectives/command-and-control/backdoor/webshell/auth::cfml-hardcoded-password-gate'
assignment = 'micro-behaviors/data/source/syntax/credential::cfml-password-literal-assignment'
session = 'micro-behaviors/os/security/auth/session::cfml-session-inequality'
cases = {
    'login': (True, True, True), 'reverse': (True, True, True),
    'assignment-only': (True, False, False), 'distant': (True, True, False),
    'form-field': (False, False, False), 'commented': (False, False, False),
    'bypass': (False, True, False), 'compass': (False, True, False), 'quoted-comparison': (True, False, False),
    'template-password': (False, True, False), 'alias-password': (False, True, False),
    'tight-operator': (True, True, True), 'elseif': (True, True, True),
    'wrong-scope': (True, False, False), 'quoted-session': (True, False, False),
    'quoted-script': (False, False, False),
}
for name, expected in cases.items():
    path = root / 'testdata/taxonomy/cfml-auth' / (name + '.cfm')
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)],
                            capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    assert obsolete not in ids, name
    assert not [t for t in traits if t['crit'] >= 4], (name, traits)
    assert (assignment in ids, session in ids, combined in ids) == expected, (name, ids)
    assert not ids.intersection({base + 'cfml-password-literal-assignment', base + 'cfml-session-password-inequality', base + 'cfml-password-session-inequality'}), (name, ids)
    assert 'objectives/command-and-control/backdoor/webshell/request::cfml-command-form-field' not in ids, name
    if name == 'form-field':
        assert 'micro-behaviors/ui/window/form-input::cfml-command-form-field' in ids, name
    print(name + ': passed')
