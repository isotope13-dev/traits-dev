#!/usr/bin/env python3
"""Verify OOB survey evidence without executing any specimen code."""
import argparse, json, shutil, subprocess, tempfile
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['cases']
# A testdata path is itself an exclusion in several rules. Scan copies with
# neutral paths so the negative cases exercise the matchers, not that exclusion.
with tempfile.TemporaryDirectory(prefix='.oob-controls-', dir=root) as staging:
    paths = []
    for case in cases:
        target = Path(staging) / case['name']
        shutil.copyfile(root / case['path'], target)
        paths.append(str(target))
    result = subprocess.run(
        [args.cleave, '--no-update-check', '--traits-dir', str(root),
         '--format=json', *paths], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    pending = result.stdout
    reports = {}
    while pending.strip():
        report, end = decoder.raw_decode(pending.lstrip())
        pending = pending.lstrip()[end:]
        for file in report['files']:
            reports[Path(file['path']).name] = file
    failures = []
    for case in cases:
        traits = reports[case['name']].get('traits', [])
        ids = {trait['id'] for trait in traits}
        for trait in case['required_traits']:
            if trait not in ids:
                failures.append(f"{case['name']}: missing {trait}")
        for trait in case['forbidden_traits']:
            if trait in ids:
                failures.append(f"{case['name']}: unexpected {trait}")
        if any(trait['crit'] >= 5 for trait in traits):
            failures.append(f"{case['name']}: unsupported hostile finding")
    if failures:
        raise SystemExit('\n'.join(failures))
print(f'{len(cases)} OOB host survey controls passed')
