"""Exercise flow and placement boundaries outside test-path suppressors."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = json.loads((Path(__file__).parent / 'cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='remote-registry-review-', dir=args.scratch) as folder:
    paths = []
    for case in cases:
        source = root / case['path']
        target = Path(folder) / source.name
        shutil.copyfile(source, target)
        paths.append(str(target))
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', *paths], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)
    remaining = result.stdout.lstrip()
    reports = []
    decoder = json.JSONDecoder()
    while remaining:
        report, consumed = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[consumed:].lstrip()
    findings = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
                for report in reports for f in report['files']}
    failures = []
    for case in cases:
        name = Path(case['path']).name
        ids = findings.get(name, set())
        for trait in case.get('matched', []):
            if trait not in ids:
                failures.append(f'{name}: missing {trait}')
        for trait in case.get('not_matched', []):
            if trait in ids:
                failures.append(f'{name}: unexpected {trait}')
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'{len(cases)} positive and near-miss controls passed')
