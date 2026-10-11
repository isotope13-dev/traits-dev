"""Check content evidence outside the intentional test-path exclusions."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch-root', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
cases = json.loads((root / 'cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='content-controls-', dir=args.scratch_root) as tmp:
    targets = []
    for name in cases:
        target = Path(tmp) / name
        shutil.copyfile(root / name, target)
        targets.append(str(target))
    env = dict(os.environ, CLEAVE_VALIDATE='0', CLEAVE_SKIP_CACHE='1')
    result = subprocess.run(
        ['cleave', '--format', 'json', *targets],
        env=env, capture_output=True, text=True, check=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    findings = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in report.get('files', []):
            findings[Path(file['path']).name] = {
                trait['id'] for trait in file.get('traits', [])
            }
    for name, case in cases.items():
        actual = findings[name]
        for trait in case['matched']:
            assert trait in actual, (name, 'missing', trait)
        for trait in case['not_matched']:
            assert trait not in actual, (name, 'unexpected', trait)
    print(f'{len(cases)} positive and near-miss controls passed')
