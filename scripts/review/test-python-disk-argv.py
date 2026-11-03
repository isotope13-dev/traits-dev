#!/usr/bin/env python3
"""Disk observations require command arrays passed to a call."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PREFIX = 'micro-behaviors/fs/disk/partition::'
CASES = {
    'parted': ("run(['parted', disk, 'mklabel', 'gpt'])", (True, False)),
    'mkfs': ("run(['mkfs.ext4', '-L', 'INSTALLER', disk])", (False, True)),
    'both': ("run(['parted', disk, 'mklabel', 'gpt'])\nrun(['mkfs', disk])", (True, True)),
    'other-parted': ("run(['parted', disk, 'print'])", (False, False)),
    'unpassed-list': ("argv = ['mkfs.ext4', disk]", (False, False)),
    'other-position': ("run(['echo', 'mkfs.ext4'])", (False, False)),
    'comment': ("# run(['parted', disk, 'mklabel'])", (False, False)),
    'string': ('''print("run(['mkfs.ext4', disk])")''', (False, False)),
}
with tempfile.TemporaryDirectory(prefix='disk-argv-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.py')
        path.write_text(source + '\n')
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        ids = {trait['id'] for trait in report.get('traits', [])}
        found = (PREFIX + 'python-parted-mklabel-argv' in ids,
                 PREFIX + 'python-mkfs-argv' in ids)
        assert found == CASES[name][1], (name, found, CASES[name][1])
print('Python disk observations match argument lists passed to calls')
