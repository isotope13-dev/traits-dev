#!/usr/bin/env python3
"""Check emitted observations for bound shell launches and placement controls."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
# Analyze content outside testdata so generic test-tree suppressors cannot
# hide the attack evidence that these standalone-payload controls exercise.
with tempfile.TemporaryDirectory(prefix='.shell-evidence-', dir=Path.cwd()) as tmp:
    original = {}
    for case in cases:
        staged = Path(tmp) / Path(case['path']).name
        shutil.copyfile(case['path'], staged)
        original[str(staged)] = case['path']
    result = subprocess.run([args.cleave, '--json', *original], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)
    files = {}
    for line in result.stdout.splitlines():
        for item in json.loads(line).get('files', []):
            files[original[item['path']]] = item
for case in cases:
    assert case['path'] in files, case['path']
    observed = {t['id'] for t in files[case['path']].get('traits', [])}
    missing = set(case['required_emitted']) - observed
    unexpected = set(case['forbidden_emitted']) & observed
    assert not missing and not unexpected, (case['case_id'], sorted(missing), sorted(unexpected))
print(f"PASS: {len(cases)} focused controls")
