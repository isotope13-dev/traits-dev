#!/usr/bin/env python3
"""Check the protected DOS builder identity signature and benign negatives."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
BUILDER = 'well-known/tool/offensive/vcl::dos-builder-compressed-fragments'
PROTECTOR = 'metadata/build/protector::hackstop-dos-marker'

def fixture():
    b = bytearray(1024)
    b[:2] = b'MZ'
    struct.pack_into('<H', b, 4, 2)
    struct.pack_into('<H', b, 8, 4)
    b[0x100:0x100+len(b'Virus...Nowh...WaReZ...compile')] = b'Virus...Nowh...WaReZ...compile'
    b[0x200:0x200+len(b'-cvcl_ ... gic_bomb')] = b'-cvcl_ ... gic_bomb'
    b[0x300:0x300+len(b'HackStop 1.10 (C) ROSE')] = b'HackStop 1.10 (C) ROSE'
    return bytes(b)

def traits(data):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'sample.bin'
        path.write_bytes(data)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        return {t['id'] for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])}

source = fixture()
assert {BUILDER, PROTECTOR} <= traits(source)
for token in [b'Virus', b'Nowh', b'WaReZ', b'compile', b'-cvcl_', b'gic_bomb']:
    assert BUILDER not in traits(source.replace(token, b'X' * len(token))), token
assert BUILDER not in traits(source.replace(b'MZ', b'ZZ', 1))
assert PROTECTOR not in traits(source.replace(b'(C) ROSE', b'(C) XXXX'))
assert BUILDER not in traits(source.replace(b'Nowh', b'Xowh', 1))
print('DOS builder identity needs the executable header and each independent fragment')
