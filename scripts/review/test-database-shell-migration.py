#!/usr/bin/env python3
"""Exercise migrated database shell and COM command evidence."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULES = (
    'micro-behaviors/process/create/shell/command-mode::sqlserver-xp-windows-command',
    'micro-behaviors/os/com/invoke::sqlserver-ole-run-method',
)
with tempfile.TemporaryDirectory(prefix='db-shell-subjects-') as tmp:
    for name, content, expected in (
        ('positive.sql', "EXEC xp_cmdshell 'cmd /c whoami';\nEXEC sp_oamethod @object, 'Run';\n", 'MATCHED'),
        ('negative.sql', 'SELECT 1;\n', 'NOT MATCHED'),
    ):
        path = Path(tmp) / name
        path.write_text(content)
        trace = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', ','.join(RULES), str(path)], text=True, capture_output=True, check=True).stdout
        for rule in RULES:
            assert f'{expected} {rule}' in trace, trace
print('Database shell and COM operations: positive and near-miss cases passed')
