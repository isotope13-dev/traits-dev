#!/usr/bin/env python3
"""Check capture, dispatch, cleanup targets, and benign boundaries."""
import argparse
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path, help='Check an existing cleave JSONL scan')
args = parser.parse_args()
if args.report:
    output = args.report.read_text()
else:
    output = subprocess.check_output(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--json']
        + [str(root / case['path']) for case in cases], text=True, cwd=root)
files = {
    Path(file['path']).name: file
    for line in output.splitlines()
    for file in json.loads(line).get('files', [])
}
for case in cases:
    file = files[Path(case['path']).name]
    ids = {trait['id'] for trait in file['traits']}
    missing = set(case['required_traits']) - ids
    forbidden = set(case['forbidden_traits']) & ids
    assert not missing, (case['path'], 'missing', missing)
    assert not forbidden, (case['path'], 'forbidden', forbidden)
    for severity, value in [('hostile', 5), ('suspicious', 4)]:
        count = sum(trait['crit'] == value for trait in file['traits'])
        assert count >= case.get('min_' + severity, 0), (case['path'], severity, count)
        if 'max_' + severity in case:
            assert count <= case['max_' + severity], (case['path'], severity, count)
print(f'PASS: {len(cases)} semantic regression controls')
