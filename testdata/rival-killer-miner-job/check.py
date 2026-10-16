#!/usr/bin/env python3
"""Supervised background jobs are not rival-killing (see README).

Run `python3 testdata/rival-killer-miner-job/check.py <scratch-directory>`.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RULE = ('objectives/impact/degrade/rival-bot/killer::'
        'killing-competing-malware')
expected = {
    'negative-job-control.sh': False,
    'positive-rival-killer.sh': True,
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for name, want in sorted(expected.items()):
    target = scratch / name
    shutil.copyfile(Path(__file__).parent / name, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    seen = {t['id'] for e in report['files'] for t in e.get('traits', [])}
    got = RULE in seen
    assert got == want, (name, sorted(seen))
    print(f'{name}: passed')
