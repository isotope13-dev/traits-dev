#!/usr/bin/env python3
"""Distinguish a redirected format instruction from unrelated batch text."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/fs/disk/partition::batch-write-format-command'
PIPE_RULE = 'micro-behaviors/fs/disk/partition::batch-pipe-to-diskpart'
CASES = {
    'append': ('echo format fs=ntfs quick label=local_ssd >> cmds', True),
    'replace': ('@echo FORMAT fs=FAT32 > disk.txt', True),
    'no-redirect': ('echo format fs=ntfs quick', False),
    'comment': ('REM echo format fs=ntfs > disk.txt', False),
    'other-command': ('echo select disk 1 > disk.txt', False),
    'separate-redirect': ('echo format fs=ntfs & echo done > disk.txt', False),
    'pipe-file': ('type cmds | diskpart', False),
    'pipe-text': ('echo list disk | diskpart | find "Online"', False),
    'comment-pipe': ('REM type cmds | diskpart', False),
}
with tempfile.TemporaryDirectory(prefix='format-text-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.bat')
        path.write_text('@echo off\n' + source + '\n')
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        found = any(trait['id'] == RULE for trait in report.get('traits', []))
        assert found == CASES[name][1], (name, found, CASES[name][1])
        piped = any(trait['id'] == PIPE_RULE for trait in report.get('traits', []))
        assert piped == (name in {'pipe-file', 'pipe-text'}), (name, piped)
print('batch format command observation requires redirected text')
