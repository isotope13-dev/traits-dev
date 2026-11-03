#!/usr/bin/env python3
"""PowerShell subprocess text stays distinct from unrelated subprocess calls."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'metadata/file/profile/process/evaluation::powershell-command-runner'
with tempfile.TemporaryDirectory(prefix='powershell-process-') as tmp:
    for name, source, expected in (
        ('powershell.py', 'import subprocess\nsubprocess.run(["powershell.exe", "-Command", "Get-Process"])\n', 'MATCHED'),
        ('git.py', 'import subprocess\nsubprocess.run(["git", "status"])\n', 'NOT MATCHED'),
    ):
        path = Path(tmp) / name
        path.write_text(source)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(path)], text=True, capture_output=True, check=True)
        assert f'{expected} {RULE}' in result.stdout, result.stdout + result.stderr
print('PowerShell subprocess profile: positive and near-miss cases passed')
