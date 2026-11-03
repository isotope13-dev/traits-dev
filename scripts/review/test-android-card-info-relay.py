#!/usr/bin/env python3
"""Check card relay evidence against size-preserving DEX mutations."""
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
    'no-card-info': (b'CardInfo', b'CardInfx'),
    'no-nfc-info': (b'NfcInfo', b'NfcInfx'),
    'no-ws-message': (b'WSMessage', b'WXMessage'),
    'no-channel': (b'CARD_INFO_CHANNEL', b'CARD_INFX_CHANNEL'),
    'no-transceive': (b'transceive', b'transceivx'),
    'no-emulation': (b'HostApduService', b'HostApduServicx'),
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
        assert ('android-card-info-websocket-relay' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Card relay rule rejects six missing DEX evidence components')
