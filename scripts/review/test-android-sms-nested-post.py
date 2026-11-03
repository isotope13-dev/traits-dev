#!/usr/bin/env python3
"""Check DEX SMS/POST call evidence against size-preserving mutations."""

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
    'no-task': (b'SendPostRequest', b'SendPastRequest'),
    'no-body': (b'getDisplayMessageBody', b'getDisplayMessageBodx'),
    'no-sender': (b'getDisplayOriginatingAddress', b'getDisplayOriginatingAddresx'),
    'no-output': (b'getOutputStream', b'getOutputStreax'),
    'no-json': (b'JSONObject', b'JSONObjecx'),
    'no-post': (b'\x04POST\x00', b'\x04P0ST\x00'),
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
        assert 'dex-sms-sender-call' in ids or report['path'].endswith('/no-sender.dex')
        assert ('android-sms-receiver-nested-http-post' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('DEX SMS relay rule rejects missing task, sender, body, JSON, output and POST')
