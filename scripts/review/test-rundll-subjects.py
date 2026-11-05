#!/usr/bin/env python3
"""Utility references must not suppress findings as signed system libraries."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
COMMAND = 'well-known/app/system/microsoft/rundll32::rundll32-command-text'
SYSTEM = 'well-known/lib/platform/microsoft-system::microsoft-known-system-context'
with tempfile.TemporaryDirectory(prefix='rundll-subjects-') as tmp:
    path = Path(tmp) / 'launch.bat'
    path.write_text('rundll32 url.dll,FileProtocolHandler https://example.org\n'
                    'rundll32 shell32.dll,Control_RunDLL\n')
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', ','.join((COMMAND, SYSTEM)), str(path)], text=True, capture_output=True, check=True)
    assert f'MATCHED {COMMAND}' in result.stdout, result.stdout + result.stderr
    assert f'NOT MATCHED {SYSTEM}' in result.stdout, result.stdout + result.stderr
print('Rundll command evidence does not establish signed system-library context')
