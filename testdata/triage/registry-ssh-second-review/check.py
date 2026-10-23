#!/usr/bin/env python3
"""Exercise SSH path/declaration placement and variable-write boundaries."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
engine = os.environ.get('CLEAVE', 'cleave')
with tempfile.TemporaryDirectory(prefix='ssh-source-controls-') as temp:
    paths = []
    for index, name in enumerate(['key-export.js', 'path-reference.js', 'empty-store.js', 'key-plant.js']):
        path = Path(temp) / str(index) / 'source.js'
        path.parent.mkdir()
        shutil.copyfile(fixtures / name, path)
        paths.append(path)
    result = subprocess.run(
        [engine, '--traits-dir', str(root), '--format', 'json', *map(str, paths)],
        capture_output=True, text=True, check=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout
    observed = {}
    while remaining.strip():
        report, consumed = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[consumed:]
        for file in report['files']:
            observed[file['path']] = {t['id']: t['crit'] for t in file['traits']}
    hostile = 'objectives/persistence/login/ssh/backdoor::js-ssh-backdoor'
    suspicious = 'objectives/persistence/login/ssh/backdoor::js-authorized-keys-short-variable-append'
    binder = 'metadata/lang/source/declaration::js-authorized-keys-binder'
    path_ref = 'micro-behaviors/fs/path/public-key::js-authorized-keys-resolve-path'
    for path in paths[:3]:
        assert hostile not in observed[str(path)], path
        assert suspicious not in observed[str(path)], path
    assert observed[str(paths[0])][binder] == 3
    assert observed[str(paths[1])][path_ref] == 3
    assert observed[str(paths[3])][hostile] == 5
    assert observed[str(paths[3])][suspicious] == 4
print('PASS: four SSH source controls')
