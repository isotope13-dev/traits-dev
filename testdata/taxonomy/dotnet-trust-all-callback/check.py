#!/usr/bin/env python3
"""Generate inert CLR metadata controls and scan them; never execute them."""
from pathlib import Path
import os
import re
import struct
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[3]
TRAIT = 'micro-behaviors/communications/tls/verify/disable::dotnet-installed-trust-all-callback'


def fixture(*, accepted=True, bound=True, setter=True, namespace=True,
            delegate=True, server=False, second=False, extra_table=False,
            cached=False, replaced=False, static=False, constructor=True):
    strings = bytearray(b'\0')

    def string(value):
        offset = len(strings)
        strings.extend(value.encode() + b'\0')
        return offset

    module = string('Control.dll')
    typename = string('RemoteCertificateValidationCallback' if delegate else 'UnrelatedDelegate')
    ns = string('System.Net.Security' if namespace else 'Other.Namespace')
    # Keep decoy text present so negatives test table relationships, rather
    # than succeeding only because an expected string vanished.
    if not delegate:
        string('RemoteCertificateValidationCallback')
    if not namespace:
        string('System.Net.Security')
    client = string('RestClient')
    restsharp = string('RestSharp')
    klass = string('ArbitraryProgram')
    field = string('cache')
    method = string('ArbitraryCallback')
    unused = string('UnrelatedTrueMethod')
    install = string('Install')
    ctor = string('.ctor' if constructor else 'UnrelatedMethod')
    if not constructor:
        string('.ctor')
    prop = string('set_' + ('Server' if server else 'Remote') + 'CertificateValidationCallback')
    parameter = string('argument')
    tables = {
        0: (1, struct.pack('<5H', 0, module, 0, 0, 0)),
        1: (2, struct.pack('<6H', 0, typename, ns, 0, client, restsharp)),
        2: (1, struct.pack('<I5H', 1, klass, 0, 0, 1, 1)),
        4: (1, struct.pack('<3H', 0x11, field, 0)),
        6: (3, b''.join(struct.pack('<I5H', rva, 0, 0x16, name, 0, 1)
                       for rva, name in [(0x2050, method), (0x2060, unused), (0x2070, install)])),
        8: (1, struct.pack('<3H', 0, 1, parameter)),
        9: (1, struct.pack('<2H', 1, 5)),
        10: (2, struct.pack('<6H', 9, ctor, 0, 17, prop, 0)),
    }
    if extra_table:
        tables[32] = (1, bytes(22))
    valid = sum(1 << t for t in tables)
    tab = struct.pack('<IBBBBQQ', 0, 2, 0, 0, 1, valid, 0)
    tab += b''.join(struct.pack('<I', count) for count, _ in tables.values())
    tab += b''.join(data for _, data in tables.values())
    # Metadata header and two stream headers (#~ and #Strings).
    header = struct.pack('<IHHII', 0x424a5342, 1, 1, 0, 12) + b'v4.0.30319\0\0'
    header += struct.pack('<HH', 0, 2)
    table_offset = len(header) + 12 + 20
    string_offset = (table_offset + len(tab) + 3) & ~3
    metadata = header + struct.pack('<II4s', table_offset, len(tab), b'#~\0\0')
    metadata += struct.pack('<II12s', string_offset, len(strings), b'#Strings\0\0\0\0')
    metadata += tab + bytes(string_offset - table_offset - len(tab)) + strings

    data = bytearray(0x1200)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x2102)
    optional = 0x98
    struct.pack_into('<H', data, optional, 0x10b)
    struct.pack_into('<III', data, optional+28, 0x400000, 0x2000, 0x200)
    struct.pack_into('<II', data, optional+56, 0x4000, 0x200)
    struct.pack_into('<H', data, optional+68, 3)
    struct.pack_into('<I', data, optional+92, 16)
    struct.pack_into('<II', data, optional+96+14*8, 0x2000, 72)
    struct.pack_into('<8sIIIIIIHHI', data, optional+224, b'.text\0\0\0',
                     0x1000, 0x2000, 0x1000, 0x200, 0, 0, 0, 0, 0x60000020)
    struct.pack_into('<IHHIIII', data, 0x200, 72, 2, 5, 0x2200, len(metadata), 1, 0)
    # One callback and one unused always-true method. Changing the callback
    # to false must fail even while the unrelated true body remains present.
    data[0x250:0x253] = bytes([0x0a, 0x17 if accepted else 0x16, 0x2a])
    data[0x260:0x263] = b'\x0a\x17\x2a'
    target = 2 if second else 1
    code = b'\x14\x14\xfe\x06' + struct.pack('<I', 0x06000000 | target)
    code += b'\x73' + struct.pack('<I', 0x0a000001)
    if cached:
        code += b'\x25\x80' + struct.pack('<I', 0x04000001)
    if replaced:
        code += b'\x26\x14'  # discard the delegate and install null instead
    code += bytes([0x28 if static else 0x6f])
    code += struct.pack('<I', 0x0a000002 if setter else 0x0a000001) + b'\x2a'
    if not bound:
        code = bytes(len(code))
    data[0x270:0x271+len(code)] = bytes([(len(code) << 2) | 2]) + code
    data[0x400:0x400+len(metadata)] = metadata
    return data


cases = [
    ('remote-true', {}, True),
    ('server-true', {'server': True}, True),
    ('different-method-token', {'accepted': False, 'second': True}, True),
    ('additional-metadata-table', {'extra_table': True}, True),
    ('cached-delegate', {'cached': True}, True),
    ('static-setter-unsupported', {'static': True, 'server': True}, False),
    ('false-with-unrelated-true', {'accepted': False}, False),
    ('unbound-true', {'bound': False}, False),
    ('wrong-setter-token', {'setter': False}, False),
    ('wrong-delegate-type', {'delegate': False}, False),
    ('wrong-delegate-namespace', {'namespace': False}, False),
    ('discarded-delegate', {'replaced': True}, False),
    ('wrong-constructor-member', {'constructor': False}, False),
]
with tempfile.TemporaryDirectory(prefix='tls-cil-controls-') as directory:
    def check(case):
        name, options, expected = case
        path = Path(directory) / (name + '.dll')
        path.write_bytes(fixture(**options))
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                 'test-rules', str(path), '--rules', TRAIT],
                                capture_output=True, text=True, check=True)
        output = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout + result.stderr)
        matched = bool(re.search(r'^MATCHED ' + re.escape(TRAIT) + r'\b', output, re.M))
        assert matched == expected, f'{name}: expected {expected}\n{output}'
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(check, cases))
print(f'{len(cases)} CLR callback controls passed')
