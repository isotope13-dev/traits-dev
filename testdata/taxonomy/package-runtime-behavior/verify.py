"""Run focused rule regressions without executing any fixture code."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch-dir', type=Path, required=True)
args = parser.parse_args()
args.scratch_dir.mkdir(parents=True, exist_ok=True)
base = Path(__file__).resolve().parent
repo = base.parents[2]
cases = json.loads((base / 'cases.json').read_text())['fixtures']
paths = []
for case in cases:
    path = base / case['file']
    if case.get('scratch_copy'):
        destination = args.scratch_dir / path.name
        shutil.copyfile(path, destination)
        path = destination
    paths.append(str(path))
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo), '--json', *paths],
                        check=True, capture_output=True, text=True)
reports = {}
for line in result.stdout.split('\n'):
    if line:
        report = json.loads(line)
        reports[report['files'][0]['path']] = report['files'][0]
checks = 0
for case, path in zip(cases, paths):
    traits = {t['id']: t['crit'] for t in reports[path]['traits']}
    for trait in case.get('required_emitted', []):
        assert trait in traits, (case['file'], 'missing', trait)
        checks += 1
    for trait in case.get('forbidden_emitted', []):
        assert trait not in traits, (case['file'], 'unexpected', trait)
        checks += 1
    if 'max_criticality' in case:
        assert max(traits.values(), default=0) <= case['max_criticality'], case['file']
        checks += 1
print(f'{len(cases)} fixtures; {checks} assertions passed')
