#!/usr/bin/env python3
"""Check SMS and banking evidence with size-preserving DEX mutations."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
changes = {
    'no-alert': (b'SMS RECEIVED', b'SMX RECEIVED'),
    'no-body': (b'getMessageBody', b'getMessageBodx'),
    'no-accessibility': (b'AccessibilityService', b'AccessibilityServicx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ['positive', *changes, 'no-banking']:
        data = source
        if name == 'no-banking':
            data, count = re.subn(b'bank|banc', b'xxxx', data, flags=re.I)
            assert count >= 8
        elif name != 'positive':
            old, new = changes[name]
            assert len(old) == len(new) and old in source, name
            data = data.replace(old, new)
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
        assert ('android-sms-telegram-banking-accessibility' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('SMS Telegram banking rule rejects four missing evidence components')
