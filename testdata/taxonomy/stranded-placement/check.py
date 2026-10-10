#!/usr/bin/env python3
"""Ensure inert references do not imply network clients or process creation."""
import json
import pathlib
import subprocess

controls = pathlib.Path(__file__).resolve().parent
root = controls.parents[2]
proc = subprocess.run(['atomscan', '--no-update', '--follow=none', '--mode', 'slow', '-f', 'json', str(controls)], cwd=root, capture_output=True, text=True)
assert proc.returncode in (0, 1, 2), proc.stderr
expected = {'url-reference.ps1', 'handle-reference.c', 'certificate-reference.py'}
seen = set()
for line in proc.stdout.splitlines():
    if not line.startswith('{'):
        continue
    for f in json.loads(line)['raw']['files']:
        name = pathlib.Path(f['path']).name
        if name not in expected:
            continue
        seen.add(name)
        traits = {t['id']: t for t in f.get('traits', [])}
        assert not any(t['crit'] == 5 for t in traits.values()), name
        assert sum(t['crit'] == 4 for t in traits.values()) <= 1, name
        if name == 'url-reference.ps1':
            assert 'micro-behaviors/communications/http/message::powershell-http-url-literal' in traits
            assert not any(k.startswith('micro-behaviors/communications/http/lib/invoke-webrequest') for k in traits), traits
        elif name == 'handle-reference.c':
            assert 'micro-behaviors/process/fd/close::close-handle-reference' in traits
            assert not any(k.startswith('micro-behaviors/process/create/spawn') for k in traits), traits
        else:
            assert traits['micro-behaviors/crypto/certificate/usage::certificate-reference-set']['crit'] == 3
        print(name + ': passed')
assert seen == expected, seen
