"""Scan copies outside test paths so production test exclusions cannot mask FPs."""
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
with tempfile.TemporaryDirectory(prefix='ccxt-controls-', dir=args.scratch) as neutral:
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
