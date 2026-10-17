#!/usr/bin/env python3
"""Security-product names with supervision APIs do not establish killing.

Build minimal PE32 inventory controls outside testdata, then verify that
neither vendor breadth nor OpenProcess/TerminateProcess imports convict.
The multi-vendor case retains the neutral API co-occurrence and survey.
"""
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]

CAPABILITY = ('micro-behaviors/process/terminate/kill::'
              'security-name-table-with-termination-apis', 3)
SURVEY = ('objectives/discovery/host/security::'
          'security-process-name-survey', 4)
SANDBOX = ('objectives/anti-analysis/sandbox-detect/tool-references::'
           'sandbox', 4)
TVNAME = ('micro-behaviors/os/service/name::teamviewer-service-name', 3)
watched = {CAPABILITY, SURVEY, SANDBOX, TVNAME}
expected = {
    'multi-vendor-inventory.exe': {CAPABILITY, SURVEY},
    'audit-inventory-negative.exe': {SANDBOX, TVNAME},
}

IMPORTS = [b'Process32NextW', b'Process32FirstW',
           b'CreateToolhelp32Snapshot', b'OpenProcess',
           b'TerminateProcess', b'CloseHandle']

POSITIVE_STRS = [b'MsMpEng.exe', b'CSFalconService.exe']
NEGATIVE_STRS = [b'MsMpEng.exe', b'wireshark', b'procmon',
                 b'TeamViewer_Service.exe']


def build_pe(path, extra_strings):
    """Minimal PE32 with a KERNEL32 import table and marker strings."""
    nsec, opt = 2, 0xe0
    size_headers, file_align = 0x200, 0x200
    rva_text, rva_idata = 0x1000, 0x2000
    off_text, off_idata = 0x200, 0x400

    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, nsec, 0, 0, 0, opt, 0x010f)
    optb = bytearray(opt)
    struct.pack_into('<H', optb, 0, 0x10b)
    struct.pack_into('<III', optb, 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', optb, 28, 0x400000, 0x3000, size_headers)
    struct.pack_into('<HH', optb, 68, 3, 0)
    struct.pack_into('<I', optb, 92, 16)
    struct.pack_into('<II', optb, 104, rva_idata, 40)
    pe += optb
    pe += struct.pack('<8sIIIIIIHHI', b'.text\x00\x00\x00', 0x200,
                      rva_text, 0x200, off_text, 0, 0, 0, 0, 0x60000020)
    pe += struct.pack('<8sIIIIIIHHI', b'.idata\x00\x00', 0x200,
                      rva_idata, 0x200, off_idata, 0, 0, 0, 0, 0x40000040)
    assert len(pe) <= size_headers
    pe += b'\x00' * (size_headers - len(pe))

    text = bytearray(b'\xc3' + b'\x00' * 31)
    for s in extra_strings:
        text += s + b'\x00'
    while len(text) < 0x200:
        text += b'\x00'
    pe += bytes(text[:0x200])

    idata = bytearray(0x200)
    ilt, iat, cursor = 0x28, 0x50, 0x78
    hn_rvas = []
    for name in IMPORTS:
        struct.pack_into('<H', idata, cursor, 0)
        idata[cursor + 2:cursor + 2 + len(name) + 1] = name + b'\x00'
        hn_rvas.append(rva_idata + cursor)
        cursor += 2 + len(name) + 1
    dlloff = cursor
    dllname = b'KERNEL32.dll\x00'
    idata[dlloff:dlloff + len(dllname)] = dllname
    struct.pack_into('<IIIII', idata, 0, rva_idata + ilt, 0, 0,
                     rva_idata + dlloff, rva_idata + iat)
    for i, rva in enumerate(hn_rvas):
        struct.pack_into('<I', idata, ilt + 4 * i, rva)
        struct.pack_into('<I', idata, iat + 4 * i, rva)
    pe += bytes(idata)
    path.write_bytes(bytes(pe))


fixtures = {
    'multi-vendor-inventory.exe': POSITIVE_STRS,
    'audit-inventory-negative.exe': NEGATIVE_STRS,
}
for fixture, strings in fixtures.items():
    target = scratch / fixture
    build_pe(target, strings)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    found = set()
    hostile = set()
    for entry in report['files']:
        hostile |= {t['id'] for t in entry['traits'] if t['crit'] == 5}
        found |= {(t['id'], t['crit']) for t in entry['traits']
                  if (t['id'], t['crit']) in watched}
    assert not hostile, (fixture, sorted(hostile))
    assert found == expected[fixture], (fixture, sorted(found))
    print(f'{fixture}: passed')
