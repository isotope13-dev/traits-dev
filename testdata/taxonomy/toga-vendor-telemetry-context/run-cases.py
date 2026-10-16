"""Scan copies outside test paths so production test exclusions cannot mask FPs.

Regression coverage for the toga-ai vendor-telemetry calibration: an
installer that writes global agent settings with full-content OTel export
plus a hardcoded collector credential fires both the base
content-telemetry-write flag and the stronger hardcoded-credential claim,
regardless of whose package name, bootstrap comment, repository URL or
collector hostname the bundle carries. Bundle identity text is
publish-credential-controlled, so it never exempts the plant. The bearer token in the fixtures is a
synthetic same-shape placeholder, not a live credential.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), CLEAVE_SKIP_CACHE='1', SCAN_NO_UPDATE='1')
with tempfile.TemporaryDirectory(prefix='toga-telemetry-controls-', dir=args.scratch) as neutral:
    for case in cases:
        target = Path(neutral) / Path(case['path']).name
        shutil.copyfile(root / case['path'], target)
        result = subprocess.run(['atomscan', '--format', 'json', str(target)],
                                env=env, capture_output=True, text=True, check=True)
        reports = [json.loads(line) for line in result.stdout.splitlines()]
        matched = {trait['id'] for report in reports for file in report['raw']['files']
                   for trait in file.get('traits', [])}
        missing = set(case['matched']) - matched
        unexpected = set(case['not_matched']) & matched
        assert not missing and not unexpected, (case['path'], missing, unexpected)
        print(f"PASS {case['path']}", flush=True)
