"""Check evaluator argument ownership without executing fixture JavaScript."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True, type=Path)
parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
args.scratch.mkdir(parents=True, exist_ok=True)
targets = []
for case in cases:
    source = root / case['path']
    target = args.scratch / source.name
    shutil.copyfile(source, target)
    targets.append(str(target))
run = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json', *targets],
    capture_output=True, text=True, check=True,
)
# Multiple inputs are emitted as consecutive JSON report objects.
remaining = run.stdout
reports = []
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:]
files = {Path(f['path']).name: f for r in reports for f in r['files']}
for case in cases:
    name = Path(case['path']).name
    traits = {t['id']: t for t in files[name].get('traits', [])}
    missing = set(case['matched']) - traits.keys()
    unexpected = set(case['not_matched']) & traits.keys()
    assert not missing, (name, 'missing', sorted(missing))
    assert not unexpected, (name, 'unexpected', sorted(unexpected))
    if name in ('returned-require.js', 'hash-and-eval.js'):
        assert all(t['crit'] < 4 for t in traits.values()), (name, 'false suspicious finding')
    print('PASS', name)
(args.scratch / 'results.json').write_text(json.dumps(reports, indent=2) + '\n')
