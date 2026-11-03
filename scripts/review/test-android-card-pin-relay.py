#!/usr/bin/env python3
"""Exercise the Android card-relay rule against modified archive copies."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1])
changes = {
    'no-pin': ('PIN de 6 dígitos'.encode(), b'PIN length removed'),
    'no-card-prompt': ('Cartão Detectado'.encode(), 'Cartão Localizado'.encode()),
    'no-channel': (b'CARD_INFO_CHANNEL', b'CARD_INFX_CHANNEL'),
    'no-socket': (b'ws://', b'wx://'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = [str(source)]
    with zipfile.ZipFile(source) as original:
        for name, (old, new) in changes.items():
            path = Path(directory) / (name + '.apk')
            replacements = 0
            with zipfile.ZipFile(path, 'w') as target:
                for info in original.infolist():
                    data = original.read(info)
                    replacements += data.count(old)
                    target.writestr(copy.copy(info), data.replace(old, new))
            assert replacements, name
            paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert ('android-nfc-relay-local-pin-prompt' in ids) == (report['path'] == str(source)), report['path']
        if report['path'].endswith(('/no-pin.apk', '/no-card-prompt.apk')):
            assert 'android-card-data-websocket-references' in ids, report['path']
print('Android relay rule rejects missing PIN, card, channel and socket evidence')
