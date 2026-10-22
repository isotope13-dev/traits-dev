"""Run static regression cases; never execute a sample."""
import json
import argparse
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--record', type=Path)
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
outputs = []
for case in cases:
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', str(root / case['path'])], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    report = json.loads(result.stdout)
    files = report.get('files', [])
    traits = {t['id'] for f in files for t in f.get('traits', [])}
    if not files and 'raw' in report:
        traits = {t['id'] for f in report['raw']['files'] for t in f.get('traits', [])}
    missing = set(case['required_emitted']) - traits
    unexpected = set(case['forbidden_emitted']) & traits
    assert not missing and not unexpected, (case['case_id'], missing, unexpected)
    outputs.append({'case': case['case_id'], 'pass': True})
    print('PASS', case['case_id'], flush=True)
if args.record:
    args.record.write_text(json.dumps(outputs, indent=2) + '\n')
