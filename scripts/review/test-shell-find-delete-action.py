#!/usr/bin/env python3
"""Distinguish find's delete action from unrelated option substrings."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/fs/search/command::delete-flag-shell'
PARENT = 'micro-behaviors/fs/delete/file/library::file-removal-api-or-command'
cases = {
    'find': ('find /tmp -type f -delete\n', True),
    'sudo': ('sudo -u user /usr/bin/find /tmp -name x -delete\n', True),
    'busybox': ('busybox find /tmp -type f -delete\n', True),
    'sudo-busybox': ('sudo busybox find /tmp -type f -delete\n', True),
    'quoted': ("find /tmp -type f '-delete'\n", True),
    'double-quoted': ('find /tmp -type f "-delete"\n', True),
    'disk-option': ('gcloud compute instances create rescue --disk=auto-delete=false,name=disk\n', False),
    'rsync-option': ('rsync --delete source destination\n', False),
    'echo': ('echo -delete\n', False),
    'comment': ('# find /tmp -type f -delete\n', False),
    'mixed': ('gcloud compute instances create rescue --disk=auto-delete=false,name=disk\nfind /tmp -type f -delete\n', True),
}
with tempfile.TemporaryDirectory(prefix='find-delete-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        p = Path(tmp) / (name + '.sh')
        p.write_text('#!/bin/sh\n' + source)
        paths.append(str(p))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for f in reports:
        name = Path(f['path']).stem
        ids = {t['id'] for t in f.get('traits', [])}
        expected = cases[name][1]
        assert (RULE in ids) == expected, (name, 'action', ids)
        assert (PARENT in ids) == expected, (name, 'parent', ids)
print('Shell find deletion is separated from unrelated auto-delete options')
