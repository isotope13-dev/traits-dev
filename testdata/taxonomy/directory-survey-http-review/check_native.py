#!/usr/bin/env python3
"""Verify UPX marker/stub distinctions and retirement of a misplaced profile."""
import concurrent.futures
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[3]
engine = os.environ.get('CLEAVE', 'cleave')
stub_id = 'well-known/dual-use/packaging/upx::upx-x86-pe-entry-stub'
writable_id = 'metadata/binary/section/header::pe-entry-in-writable-section'
marker_id = 'metadata/build/protector::upx-packing-token-reference'
old = 'objectives/command-and-control/dropper/file-exec/spawn::upx-renamed-section-packer-evidence'

def fixture(writable, marker, stub):
    image = bytearray(4608)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', image, optional, 0x10b)
    for off, value in {4:4096,16:4096,20:4096,28:0x400000,32:4096,36:512,
                       56:8192,60:512,72:0x100000,76:4096,80:0x100000,
                       84:4096,92:16}.items():
        struct.pack_into('<I', image, optional+off, value)
    struct.pack_into('<H', image, optional+40, 5)
    struct.pack_into('<H', image, optional+48, 5)
    struct.pack_into('<H', image, optional+68, 3)
    section = optional + 224
    image[section:section+8] = b'.text\0\0\0'
    struct.pack_into('<IIII', image, section+8,4096,4096,4096,512)
    struct.pack_into('<I', image, section+36,0xe0000020 if writable else 0x60000020)
    image[512] = 0xc3
    if stub:
        image[512:524] = bytes.fromhex('60 BE 00 20 40 00 8D BE 00 F0 FF FF')
    if marker:
        value = b'packer UPX! marker\0'
        image[600:600+len(value)] = value
    return image

cases = [('marker', True, True, False),
         ('stub', True, False, True),
         ('writable-only', True, False, False),
         ('marker-readonly', False, True, False),
         ('stub-readonly', False, False, True),
         ('dotnet-token-references', True, False, False)]
with tempfile.TemporaryDirectory(prefix='upx-context-controls-', dir=repo) as temporary:
    def run(case):
        name,writable,marker,stub=case
        path=Path(temporary,name+'.exe')
        data = fixture(writable,marker,stub)
        if name == 'dotnet-token-references':
            value = b'HttpClient\0GetStringAsync\0GetByteArrayAsync\0'
            data[700:700+len(value)] = value
        path.write_bytes(data)
        proc=subprocess.run([engine,'--traits-dir',str(repo),str(path),'--format','json'],capture_output=True,text=True)
        assert proc.returncode==0,(name,proc.stderr)
        traits=[t for f in json.loads(proc.stdout)['files'] for t in f.get('traits',[])]
        ids={t['id'] for t in traits}
        assert old not in ids, (name, ids)
        assert (stub_id in ids) == stub, (name, ids)
        assert (writable_id in ids) == writable, (name, ids)
        assert (marker_id in ids) == marker, (name, ids)
        gets = {'micro-behaviors/communications/http/get::getstringasync',
                'micro-behaviors/communications/http/get::getbytearrayasync'}
        assert ids & gets == (gets if name == 'dotnet-token-references' else set()), (name, ids)
        for t in traits:
            if t['id'] in {stub_id, writable_id, marker_id}:
                assert t['crit'] == 3, (name, t)
        return name+': PASS'
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(run,cases):
            print(result,flush=True)
