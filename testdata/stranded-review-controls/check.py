#!/usr/bin/env python3
"""Check inert names, crypto direction, and standalone ransom wording."""
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[2]
controls = pathlib.Path(__file__).resolve().parent
proc = subprocess.run(['atomscan', '--no-update', '--follow=none', '--mode', 'slow', '-f', 'json', str(controls)], cwd=root, capture_output=True, text=True)
assert proc.returncode in (0, 1, 2), proc.stderr
files = [f for line in proc.stdout.splitlines() if line.startswith('{') for f in json.loads(line)['raw']['files']]
seen = set()
for f in files:
    name = pathlib.Path(f['path']).name
    if name not in {'functions-only.ps1', 'final-block.cs', 'psransom-message.ps1', 'unrelated-filecrypto.ps1', 'ordinary-encryption.ps1'}:
        continue
    seen.add(name)
    traits = {t['id']: t for t in f.get('traits', [])}
    assert not any(t['crit'] == 5 for t in traits.values()), name
    assert sum(t['crit'] == 4 for t in traits.values()) <= 1, name
    if name == 'final-block.cs':
        assert 'micro-behaviors/crypto/cipher::dotnet-transform-final-block' in traits
        assert not any('symmetric/decrypt' in k or 'symmetric/encrypt' in k for k in traits), traits
    assert 'well-known/tool/offensive/psransom::file-encryption-payload' not in traits
    print(name + ': passed')
assert len(seen) == 5, seen
