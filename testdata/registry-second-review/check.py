#!/usr/bin/env python3
"""Static controls, staged outside testdata to avoid path-based suppressors."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='.review-controls-', dir='.') as staging:
    staged = []
    for case in cases:
        target = Path(staging) / Path(case['path']).name
        shutil.copyfile(case['path'], target)
        staged.append(str(target))
    result = subprocess.run(
        ['cleave', '--traits-dir', '.', '--format', 'json', *staged],
        check=False, capture_output=True, text=True,
    )
if result.returncode:
    raise RuntimeError(result.stdout + result.stderr)
reports = []
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
while remaining:
    item, consumed = decoder.raw_decode(remaining)
    reports.append(item)
    remaining = remaining[consumed:].lstrip()
files = [f for item in reports for f in item['files']]
for case in cases:
    file = next(f for f in files if Path(f['path']).name == Path(case['path']).name)
    traits = {t['id']: t for t in file['traits']}
    assert set(case['matched']) <= traits.keys(), (case['path'], 'missing', set(case['matched']) - traits.keys())
    assert not set(case['not_matched']) & traits.keys(), (case['path'], 'unexpected', set(case['not_matched']) & traits.keys())
    for ident, criticality in case['expected_criticality'].items():
        assert traits[ident]['crit'] == criticality, (case['path'], ident, traits[ident]['crit'])
    hostile = [t['id'] for t in file['traits'] if t['crit'] == 5]
    assert len(hostile) <= case['max_hostile'], (case['path'], hostile)
    if case['max_hostile'] == 0:
        suspicious = [t['id'] for t in file['traits'] if t['crit'] == 4]
        assert len(suspicious) <= 1, (case['path'], suspicious)
    obsolete = {
        'objectives/discovery/system/fingerprint/cicd::runner-fingerprinting',
        'objectives/supply-chain/trojanized/app/package::suspicious-stealer-discovery',
        'objectives/supply-chain/install-hook/dropper/shell::github-ci-identity-fields',
    }
    assert not obsolete & traits.keys(), (case['path'], obsolete & traits.keys())
    print(case['path'], 'PASS', len(hostile), 'hostile')
