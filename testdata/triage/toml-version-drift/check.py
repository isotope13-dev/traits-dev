#!/usr/bin/env python3
"""Retain real XOR and loader coverage while rejecting mathematical prose."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
xor = 'micro-behaviors/data/arithmetic::python-xor-expression'
loader = 'objectives/anti-static/obfuscation/encoding/xor::bytewise-xor-base64-exec-loader'
cases = [
    (here / 'range-prose.py', set(), {xor}),
    (here / 'range-with-xor.py', {xor}, set()),
    (here / 'numeric-xor.py', {xor}, set()),
    (here / 'xor-beside-range-string.py', {xor}, set()),
    (root / 'testdata/elements-version-drift/xor-expression.py', {xor}, set()),
    (root / 'testdata/elements-version-drift/xor-operator.py', {xor}, set()),
    (root / 'testdata/elements-version-drift/xor-string.py', set(), {xor}),
    (root / 'testdata/taxonomy/ty-version-drift/xor.py', {xor}, set()),
    (root / 'testdata/taxonomy/ty-version-drift/diagnostic.snap', set(), {xor}),
    (root / 'testdata/taxonomy/oxbar-triage/xor-exec-loader.py', {xor, loader}, set()),
    (root / 'testdata/triage/first-review/loader-xor-near-exec.py', {
        xor,
        'objectives/anti-static/obfuscation/eval/scripting/decode::xor-layered-python-packer',
    }, set()),
]
output = subprocess.check_output([
    os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
    '--format', 'json', *(str(path) for path, _, _ in cases),
], text=True, cwd=root)
decoder = json.JSONDecoder()
files = {}
while output.strip():
    output = output.lstrip()
    report, end = decoder.raw_decode(output)
    output = output[end:]
    for file in report['files']:
        files[Path(file['path']).resolve()] = {
            trait['id'] for trait in file.get('traits', [])
        }
for path, required, forbidden in cases:
    actual = files[path.resolve()]
    assert required <= actual, (path, 'missing', required - actual)
    assert not forbidden & actual, (path, 'unexpected', forbidden & actual)
print(f'PASS: {len(cases)} mathematical-prose, XOR and loader controls')
