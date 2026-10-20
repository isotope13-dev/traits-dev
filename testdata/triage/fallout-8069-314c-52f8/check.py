#!/usr/bin/env python3
"""Exercise the reviewed trait boundaries using benign controls and near misses."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='review-controls-', dir=args.scratch) as tmp:
    tmp = Path(tmp)
    targets = []
    for case in cases:
        target = tmp / case['name']
        targets.append(str(target))
        if 'files' in case:
            with zipfile.ZipFile(target, 'w') as archive:
                for name, content in case['files'].items():
                    archive.writestr(name, content)
        else:
            target.write_text(case['source'])
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(root), '--format', 'jsonl', *targets],
        text=True, capture_output=True, check=True)
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    by_name = {Path(report['files'][0]['path']).name: report for report in reports}
    assert len(by_name) == len(cases), (len(by_name), len(cases), result.stderr)
    for case in cases:
        report = by_name[case['name']]
        traits = {trait['id']: trait for f in report['files'] for trait in f.get('traits', [])}
        for expected in case.get('must', []):
            assert expected in traits, (case['name'], 'missing', expected, result.stderr)
        for unexpected in case.get('absent', []):
            assert unexpected not in traits, (case['name'], 'unexpected', unexpected)
        if 'max_crit' in case:
            assert all(t['crit'] <= case['max_crit'] for t in traits.values()), (
                case['name'], [(t['id'], t['crit']) for t in traits.values() if t['crit'] > case['max_crit']])
        print('PASS', case['name'], flush=True)
print(f'{len(cases)} reviewed boundary controls passed')
