"""Static rule checks; specimen commands are never executed."""
import argparse
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--reports', nargs='*', type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
if args.reports:
    text = '\n'.join(p.read_text() for p in args.reports)
else:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'jsonl', *[str(ROOT / c['path']) for c in cases]],
        capture_output=True, text=True, check=True,
    )
    assert not result.stderr.strip(), result.stderr
    text = result.stdout
files = {str(Path(f['path']).resolve()): f
         for line in text.splitlines() if line.strip()
         for f in json.loads(line)['files']}
records = []
for case in cases:
    file = files[str((ROOT / case['path']).resolve())]
    traits = {t['id']: t['crit'] for t in file.get('traits', [])}
    assert set(case.get('matched', [])) <= traits.keys(), (case['path'], 'missing')
    assert not set(case.get('not_matched', [])) & traits.keys(), (case['path'], 'unexpected')
    hostile = sum(c == 5 for c in traits.values())
    suspicious = sum(c == 4 for c in traits.values())
    if 'max_hostile' in case:
        assert hostile <= case['max_hostile'], (case['path'], hostile)
    if case.get('no_process_creation'):
        assert not any(t.startswith('micro-behaviors/process/create/') for t in traits), case
    records.append({'path': case['path'], 'hostile': hostile,
                    'suspicious': suspicious, 'passed': True})
if args.output:
    args.output.write_text(json.dumps(records, indent=2) + '\n')
print(f'{len(records)} static coverage and boundary checks passed')
