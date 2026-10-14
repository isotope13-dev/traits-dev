#!/usr/bin/env python3
"""Verify triage controls without executing any specimen code.

Archive fixtures (miniature .tgz packages) scan as npm archives whose member
files each report findings, so results are unioned across every file whose
path belongs to the fixture. Required hostile findings are expected — the
runner only rejects hostile findings a case did not ask for.
"""
import argparse, json, shutil, subprocess, tempfile
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['cases']
# A testdata path is itself an exclusion in several rules. Scan copies with
# neutral paths so the negative cases exercise the matchers, not that exclusion.
with tempfile.TemporaryDirectory(prefix='.triage-controls-', dir=root) as staging:
    staged = {}
    for case in cases:
        target = Path(staging) / case['name']
        shutil.copyfile(root / case['path'], target)
        staged[case['name']] = str(target)
    result = subprocess.run(
        [args.cleave, '--no-update-check', '--traits-dir', str(root),
         '--format=json', *staged.values()], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    pending = result.stdout
    findings = {name: {} for name in staged}
    while pending.strip():
        report, end = decoder.raw_decode(pending.lstrip())
        pending = pending.lstrip()[end:]
        for file in report['files']:
            for name, path in staged.items():
                if file['path'].startswith(path):
                    for trait in file.get('traits', []):
                        findings[name][trait['id']] = trait
    failures = []
    for case in cases:
        ids = findings[case['name']]
        for trait in case['required_traits']:
            if trait not in ids:
                failures.append(f"{case['name']}: missing {trait}")
        for trait in case['forbidden_traits']:
            if trait in ids:
                failures.append(f"{case['name']}: unexpected {trait}")
        for tid, trait in ids.items():
            if trait['crit'] >= 5 and tid not in case['required_traits']:
                failures.append(f"{case['name']}: unsupported hostile finding {tid}")
    if failures:
        raise SystemExit('\n'.join(failures))
print(f'{len(cases)} controls passed')
