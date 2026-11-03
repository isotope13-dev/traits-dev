#!/usr/bin/env python3
"""Check independent evidence requirements for the native asset installer."""
from copy import copy
import json
import os
from pathlib import Path
import subprocess
import struct
import sys
import tempfile
from zipfile import ZipFile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
changes = {
    'no-decrypt': (b'_decryptAssets__', b'_decryptAssetx__'),
    'no-install': (b'_installPackage__', b'_installPackagx__'),
    'no-start': (b'_startInstallationOnce__', b'_startInstallationOncx__'),
}
with tempfile.TemporaryDirectory() as directory, ZipFile(sys.argv[1]) as original:
    paths = []
    for name in ('positive', *changes, 'no-opaque-assets', 'no-install-permission', 'no-unknown-method'):
        path = Path(directory) / (name + '.apk')
        changed = 0
        with ZipFile(path, 'w') as output:
            patched_name = None
            for entry in original.infolist():
                info = copy(entry)
                if entry.compress_type not in (0, 8):
                    info.compress_type = 0
                    data = b'unsupported-method-placeholder'
                    patched_name = info.filename.encode()
                else:
                    data = original.read(entry)
                if name in changes and entry.filename.endswith('.so'):
                    old, new = changes[name]
                    assert len(old) == len(new)
                    changed += data.count(old)
                    data = data.replace(old, new)
                if name == 'no-install-permission' and entry.filename == 'AndroidManifest.xml':
                    old = 'android.permission.REQUEST_INSTALL_PACKAGES'.encode('utf-16le')
                    new = 'android.permission.REQUEST_INSTALL_PACKAGEX'.encode('utf-16le')
                    changed += data.count(old)
                    data = data.replace(old, new)
                if name == 'no-opaque-assets' and entry.filename.startswith('assets/') and '.' not in entry.filename.rsplit('/', 1)[-1]:
                    info.filename += '.bin'
                    changed += 1
                output.writestr(info, data)
        assert name in ('positive', 'no-unknown-method') or changed, name
        assert patched_name
        if name != 'no-unknown-method':
            raw = bytearray(path.read_bytes())
            search_from = 0
            for sig, offset, name_offset in ((b'PK\x03\x04', 8, 30), (b'PK\x01\x02', 10, 46)):
                name_pos = raw.find(patched_name, search_from)
                while name_pos >= 0 and raw[name_pos - name_offset:name_pos - name_offset + 4] != sig:
                    name_pos = raw.find(patched_name, name_pos + 1)
                assert name_pos >= 0
                pos = name_pos - name_offset
                search_from = name_pos + len(patched_name)
                struct.pack_into('<H', raw, pos + offset, 65000)
            path.write_bytes(raw)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert ('android-native-opaque-asset-installer-vpn' in ids) == report['path'].endswith('/positive.apk'), report['path']
print('Native asset installer rule rejects six missing evidence components')
