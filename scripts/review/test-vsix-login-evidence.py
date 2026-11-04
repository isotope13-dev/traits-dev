#!/usr/bin/env python3
"""Keep private-key form and dynamic-login URL observations distinct."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
field = 'const html = `<input id="privateKeyInput" type="password">`;\n'
route = 'const url = `/users/login/${key}`;\n'
flow = ('const keyInput = document.getElementById("privateKeyInput");\n'
        'const key = keyInput.value.trim();\n'
        'fetch(`/users/login/${key}`);\n')
cases = {'both.js': field + route, 'field.js': field, 'route.js': route,
         'flow.js': flow, 'other-input.js': flow.replace('privateKeyInput', 'usernameInput'),
         'other-value.js': flow.replace('keyInput.value', 'otherInput.value'),
         'other-sink.js': flow.replace('/login/${key}', '/login/${other}')}
with tempfile.TemporaryDirectory(prefix='vsix-login-evidence-') as temp:
    root = Path(temp)
    for name, source in cases.items():
        (root / name).write_text(source)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / name) for name in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    combined = 'micro-behaviors/ui/controls/credential::private-key-field-and-dynamic-login-path'
    old = 'objectives/credential-access/capture/network::private-key-in-login-url-path'
    bound = 'micro-behaviors/communications/http/request/credentials/application-state::private-key-input-login-url'
    assert combined in found['both.js']
    assert combined not in found['field.js'] and combined not in found['route.js']
    assert all(old not in ids for ids in found.values())
    assert bound in found['flow.js']
    assert all(bound not in found[n] for n in ('other-input.js', 'other-value.js', 'other-sink.js'))
    print('Login-path and private-key form findings report co-occurrence only.')
