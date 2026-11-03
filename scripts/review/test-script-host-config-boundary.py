#!/usr/bin/env python3
"""Constructing a WScript command does not establish a shell launch."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
CONFIG = 'micro-behaviors/process/config/launch::rust-wscript-command'
EXEC = 'metadata/file/profile/process/shell::shell-execution-comp'
with tempfile.TemporaryDirectory(prefix='script-host-config-') as tmp:
    path = Path(tmp) / 'main.rs'
    path.write_text('fn main() { let cmd = std::process::Command::new("wscript.exe"); }\n')
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', ','.join((CONFIG, EXEC)), str(path)], text=True, capture_output=True, check=True)
    assert f'MATCHED {CONFIG}' in result.stdout, result.stdout + result.stderr
    assert f'NOT MATCHED {EXEC}' in result.stdout, result.stdout + result.stderr
print('WScript command construction does not imply shell execution')
