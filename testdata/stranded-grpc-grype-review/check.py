#!/usr/bin/env python3
"""Static-call, provenance and severity controls; never runs Go fixtures."""
import json
import os
import subprocess
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / 'cases.json').read_text())
temporary = tempfile.TemporaryDirectory()
targets = []
for c in cases:
    if 'compile' in c:
        target = Path(temporary.name) / c['file']
        subprocess.run([os.environ.get('CC', 'cc'), '-O0', str(HERE / c['compile']), '-o', str(target)], check=True)
    else:
        target = HERE / c['file']
    targets.append(str(target))
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *targets], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
files = {}
text = result.stdout
while text.strip():
    report, end = json.JSONDecoder().raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for f in report['files']:
        files[Path(f['path']).name] = {t['id']: t for t in f.get('traits', [])}
checks = 0
for c in cases:
    found = files[Path(c['file']).name]
    for id in c['present']:
        assert id in found, (c['file'], 'missing', id)
        assert found[id]['crit'] == c.get('criticality', 3), (c['file'], id, found[id]['crit'])
        checks += 2
    for id in c['absent']:
        assert id not in found, (c['file'], 'unexpected', id)
        checks += 1
print(f'PASS: {checks} call, provenance and severity assertions')

temporary.cleanup()
