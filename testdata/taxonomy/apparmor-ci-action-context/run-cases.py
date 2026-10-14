"""Scan copies outside test paths so production test exclusions cannot mask FPs.

Regression coverage for the vitess setup-mysql false positive: AppArmor
relaxation inside a reusable composite action under .github/actions/ is the
same ephemeral-runner CI provisioning context as a .github/workflows/ step,
so apparmor-disabled must stay silent there (manifest node and extracted
run-step alike) while still firing on a host script with no CI context.

Unlike the flat copiers, this runner preserves the fixture tree below
files/: the benign context lives in the directory path, so flattening would
destroy the very signal under test.
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
with tempfile.TemporaryDirectory(prefix='apparmor-ci-controls-', dir=args.scratch) as neutral:
    for case in cases:
        source = root / case['path']
        rel = source.relative_to(Path(__file__).with_name('files'))
        target = Path(neutral) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        result = subprocess.run(['atomscan', '--format', 'json', str(target)],
                                env=env, capture_output=True, text=True, check=True)
        reports = [json.loads(line) for line in result.stdout.splitlines()]
        matched = {trait['id'] for report in reports for file in report['raw']['files']
                   for trait in file.get('traits', [])}
        missing = set(case['matched']) - matched
        unexpected = set(case['not_matched']) & matched
        assert not missing and not unexpected, (case['path'], missing, unexpected)
        print(f"PASS {case['path']}", flush=True)
