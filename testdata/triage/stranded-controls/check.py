"""Check renamed attack controls and harmless lookalikes against local traits."""
import json
import os
from pathlib import Path
import subprocess
import sys

cases = json.loads(Path(__file__).with_name('cases.json').read_text())
env = dict(os.environ, CLEAVE_VALIDATE='0', SCAN_FETCH='none')
failures = []
for case in cases['fixtures']:
    result = subprocess.run(
        ['cleave', '--json', case['path']], capture_output=True, text=True,
        env=env, check=True,
    )
    report = json.loads(result.stdout)
    traits = {trait['id'] for f in report['files'] for trait in f.get('traits', [])}
    missing = set(case['matched']) - traits
    unexpected = set(case['not_matched']) & traits
    if missing or unexpected:
        failures.append((case['path'], sorted(missing), sorted(unexpected)))
    print(case['path'], 'FAIL' if missing or unexpected else 'PASS', flush=True)
if failures:
    print(json.dumps(failures, indent=2))
    sys.exit(1)
