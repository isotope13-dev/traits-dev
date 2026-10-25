#!/usr/bin/env python3
"""Check response placement, source-field boundaries and preserved consumers."""
import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--baseline', type=Path)
args = parser.parse_args()
MOVED = {
    'micro-behaviors/communications/http/lib/requests::raise-for-status':
        'micro-behaviors/communications/http/response::raise-for-status',
    'micro-behaviors/communications/http/response::native-status-field-pair':
        'metadata/lang/source/syntax/key-value::native-status-service-target-fields',
}
STATUS, FIELDS = MOVED.values()
BEACON = 'objectives/command-and-control/beacon/network/http::native-status-http-beacon'
targets = list(HERE.glob('*.py')) + list(HERE.glob('*.c'))
targets.remove(Path(__file__).resolve())
targets += [ROOT / 'testdata/suspicious/owa-bearer-replay-controls.py',
            ROOT / 'testdata/benign/device-enrollment-controls.py',
            ROOT / 'testdata/benign/service-login-token-exchange.py']
targets += list((ROOT / 'testdata/stranded-review/fixtures').glob('*'))

def scan(traits):
    result = subprocess.run(['cleave', '--traits-dir', str(traits), '--format',
                             'jsonl', *map(str, targets)],
                            text=True, capture_output=True)
    assert result.returncode in (0, 1), result.stderr
    assert not result.stderr.strip(), result.stderr
    reports = {}
    for line in result.stdout.splitlines():
        for file in json.loads(line)['files']:
            reports[Path(file['path']).name] = {
                t['id']: t['crit'] for t in file.get('traits', [])}
    return reports

after = scan(ROOT)
for name, present, absent in [
    ('response-client.py', [STATUS], [FIELDS]),
    ('status-name-only.py', [], [STATUS]),
    ('service-status.c', [FIELDS], [STATUS, BEACON]),
    ('service-target-only.c', [], [FIELDS, BEACON]),
    ('beacon-status.c', [FIELDS, BEACON], []),
    ('owa-bearer-replay-controls.py', [STATUS], []),
]:
    got = after[name]
    assert set(present) <= got.keys(), (name, 'missing', set(present) - got.keys())
    assert not (set(absent) & got.keys()), (name, 'unexpected', set(absent) & got.keys())
    assert not (MOVED.keys() & got.keys()), (name, 'old ID')
if args.baseline:
    before = scan(args.baseline)
    for name, traits in before.items():
        expected = {MOVED.get(k, k): v for k, v in traits.items()}
        assert expected == after[name], (name, 'coverage changed',
            expected.keys() - after[name].keys(), after[name].keys() - expected.keys())
print(f'PASS: placement controls and {len(after)} fixture comparisons')
