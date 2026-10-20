#!/usr/bin/env python3
"""Check the behavior boundaries; never execute the fixture scripts."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
if args.report:
    data = args.report.read_text()
else:
    # Filename exclusions for test trees must not silence the observations
    # under test. Preserve member layout in a temporary non-test directory.
    with tempfile.TemporaryDirectory(prefix='.stranded-controls-', dir=root) as tmp:
        paths = []
        fixture_root = Path(__file__).resolve().parent
        for case in cases:
            source = root / case['path']
            target = Path(tmp) / source.relative_to(fixture_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            paths.append(str(target))
        data = subprocess.check_output([args.cleave, '--traits-dir', str(root), '--json'] + paths, text=True, cwd=root)
files = {}
for line in data.splitlines():
    report = json.loads(line)
    for file in report.get('raw', report).get('files', []):
        files[Path(file['path']).name] = file
for case in cases:
    file = files[Path(case['path']).name]
    traits = {t['id']: t for t in file.get('traits', [])}
    for trait in case.get('matched', []):
        assert trait in traits, (case['path'], 'missing', trait)
    for trait in case.get('not_matched', []):
        assert trait not in traits, (case['path'], 'unexpected', trait)
    if case.get('no_hostile'):
        assert all(t['crit'] < 5 for t in traits.values()), case['path']
    if 'max_suspicious' in case:
        assert sum(t['crit'] == 4 for t in traits.values()) <= case['max_suspicious'], case['path']
print(f'{len(cases)} behavior-boundary fixtures passed')
