#!/usr/bin/env python3
"""Self-cleaning maintenance installers retain dual-use traits, without hostility."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
ns = 'objectives/persistence/system/scheduled-task::'
expected = {
    'maintenance-installer.py': ns + 'python-self-deleting-archive-task-loader',
    'maintenance-installer.ps1': ns + 'powershell-cmdlet-self-deleting-archive-task-loader',
}
for name, required in expected.items():
    target = scratch / name
    shutil.copy2(HERE / name, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'jsonl', str(target)],
        text=True, capture_output=True, check=True,
    )
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    traits = [t for report in reports for f in report['files'] for t in f['traits']]
    assert required in {t['id'] for t in traits}, (name, 'lost dual-use coverage')
    assert not [t for t in traits if t['crit'] == 5], (name, 'unexpected hostility')
    print(name + ': retained suspicious task-loader finding; zero hostile')
