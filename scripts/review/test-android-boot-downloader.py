#!/usr/bin/env python3
"""Check Android boot-downloader clues against size-preserving DEX edits."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
changes = {
    'no-boot': (b'android.intent.action.BOOT_COMPLETED', b'android.intent.action.BOOT_COMPLETEX'),
    'no-exec': (b'\x04exec\x00', b'\x04exex\x00'),
    'no-busybox': (b'busybox wget', b'busybox wgeX'),
    'no-toybox': (b'toybox wget', b'toybox wgeX'),
    'no-pipeline': (b'| sh', b'| xx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, change in [('positive', None), *changes.items()]:
        data = source
        if change:
            old, new = change
            assert len(old) == len(new) and old in source, name
            data = source.replace(old, new)
        path = Path(directory) / (name + '.dex')
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert 'dex-runtime-exec-call' in ids or report['path'].endswith('/no-exec.dex')
        assert ('android-boot-downloader-exec-clues' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Android boot downloader rejects missing boot, exec, fallback or pipeline clues')
