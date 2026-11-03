#!/usr/bin/env python3
"""Distinguish .NET process configuration from launch and PowerShell commands."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='process-start-taxonomy-') as tmp:
    root = Path(tmp)
    common = 'using System.Diagnostics;\nclass C { static void Main() { var proc = new Process();'
    cases = {'setup.cs': common + ' } }\n', 'launch.cs': common + ' proc.Start(); } }\n',
             'start.ps1': 'Start-Process -FilePath calc.exe\n'}
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(root / name) for name in cases)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    setup = 'micro-behaviors/process/create/subprocess/configure::dotnet-process-object-creation'
    start = 'micro-behaviors/process/create/subprocess/launch::dotnet-process-instance-start-call'
    assert setup in ids['setup.cs'] and start not in ids['setup.cs']
    assert setup in ids['launch.cs'] and start in ids['launch.cs']
    assert 'micro-behaviors/process/create/command::start-process-symbol-call' in ids['start.ps1']
    print('Process object setup, launch and PowerShell invocation are distinguished.')
