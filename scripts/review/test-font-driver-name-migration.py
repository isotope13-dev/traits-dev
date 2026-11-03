#!/usr/bin/env python3
"""A pair of names is a profile, not evidence of staging."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'metadata/file/profile/path-reference::fontdrvhost-myagent-clues'
with tempfile.TemporaryDirectory(prefix='font-driver-names-') as directory:
    for name, content, expected in (
        ('both.ps1', 'C:\\Windows\\fontdrvhost.exe\nfontdrvhost.MyAgent\n', 'MATCHED'),
        ('one.ps1', 'C:\\Windows\\fontdrvhost.exe\n', 'NOT MATCHED'),
    ):
        path = Path(directory) / name
        path.write_text(content)
        trace = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(path)], text=True, capture_output=True, check=True).stdout
        assert f'{expected} {RULE}' in trace, trace
print('Font driver name profile: paired and single-name cases passed')
