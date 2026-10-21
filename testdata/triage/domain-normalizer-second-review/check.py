"""Focused trait checks; copy fixtures out of test-path suppressor scope."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
base = Path(__file__).resolve().parent
cases = json.loads((base / 'cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='normalizer-controls-', dir=args.scratch) as folder:
    destination = Path(folder)
    for case in cases:
        shutil.copyfile(base / Path(case['path']).name, destination / Path(case['path']).name)
    result = subprocess.run([args.cleave, '--traits-dir', str(Path.cwd()), '--format', 'json', str(destination)], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    reports, remainder = [], result.stdout
    decoder = json.JSONDecoder()
    while remainder.strip():
        report, length = decoder.raw_decode(remainder.lstrip())
        reports.append(report)
        remainder = remainder.lstrip()[length:]
    files = {Path(file['path']).name: file for report in reports for file in report['files'] if file.get('pid') is None}
    for case in cases:
        file = files[Path(case['path']).name]
        emitted = {trait['id'] for trait in file.get('traits', [])}
        missing = set(case['required_emitted']) - emitted
        forbidden = set(case['forbidden_emitted']) & emitted
        assert not missing and not forbidden, (case['case_id'], sorted(missing), sorted(forbidden))
        assert all(trait['crit'] < 5 for trait in file.get('traits', [])), case['case_id']
        if Path(case['path']).suffix in {'.lua', '.go', '.bat'} and case['case_id'] != 'launch-log.bat':
            assert all(trait['crit'] < 4 for trait in file.get('traits', [])), case['case_id']
        assert not any(trait['id'].startswith('well-known/lib/network/golang-x-net') for trait in file.get('traits', [])), case['case_id']
        print('PASS', case['case_id'])
print(f'{len(cases)} controls passed')
