"""Scan static controls outside the test tree; never execute their contents."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']

def check(case):
    source = ROOT / case['path']
    target = args.scratch / source.name
    shutil.copyfile(source, target)
    result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--json', str(target)],
                            text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    actual = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    missing = set(case['required_emitted']) - actual
    unexpected = set(case['forbidden_emitted']) & actual
    assert not (missing or unexpected), (case['case_id'], missing, unexpected)
    return {'case': case['case_id'], 'passed': True}

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, cases))
print(json.dumps(results, indent=2))
