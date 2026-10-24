"""Inert PE controls; run with a scratch output directory. Never executes PEs."""
import base64
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
D = 'micro-behaviors/os/security/defender::base64-path-exclusion-command'
R = 'micro-behaviors/os/recovery::base64-reagentc-disable-command'
T = ('objectives/privilege-escalation/token-manipulation::'
     'lsass-token-duplication-impersonation-profile')
N = 'micro-behaviors/fs/file/rename::go-x86-file-rename-info-call-setup'
X = 'micro-behaviors/fs/delete/file/library::go-x86-delete-disposition-call-setup'
TOKEN = bytes.fromhex(
    'C7 44 24 04 FF 01 0F 00 C7 44 24 08 00 00 00 00 '
    'C7 44 24 0C 02 00 00 00 C7 44 24 10 01 00 00 00 '
    '8D 44 24 2C 89 44 24 14 E8 00 00 00 00')
RENAME = bytes.fromhex(
    '89 0C 24 C7 44 24 04 03 00 00 00 89 5C 24 08 '
    '89 44 24 0C E8 00 00 00 00')
DELETE = bytes.fromhex(
    'C7 84 24 F4 02 00 00 01 00 00 00 89 04 24 '
    'C7 44 24 04 04 00 00 00 8D 84 24 F4 02 00 00 '
    '89 44 24 08 C7 44 24 0C 04 00 00 00 E8 00 00 00 00')
APIS = b'lsass.exe\0OpenProcessToken\0DuplicateTokenEx\0ImpersonateLoggedOnUser\0'


def pe(code=b'\xc3', data=b'', data_name='.rdata'):
    h = bytearray(512)
    h[:2] = b'MZ'
    struct.pack_into('<I', h, 60, 128)
    h[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', h, 132, 0x14c, 2, 0, 0, 0, 224, 0x102)
    o = 152
    struct.pack_into('<H', h, o, 0x10b)
    struct.pack_into('<I', h, o+16, 0x1000)
    struct.pack_into('<I', h, o+28, 0x400000)
    struct.pack_into('<II', h, o+32, 4096, 512)
    struct.pack_into('<II', h, o+56, 12288, 512)
    struct.pack_into('<H', h, o+68, 3)
    struct.pack_into('<I', h, o+92, 16)
    for i, name, blob, flags in [(0, '.text', code, 0x60000020),
                                  (1, data_name, data, 0x40000040)]:
        assert len(blob) <= 512
        struct.pack_into('<8sIIIIIIHHI', h, 376+i*40,
                         name.encode(), max(1, len(blob)), 4096*(i+1),
                         512, 512*(i+1), 0, 0, 0, 0, flags)
    return bytes(h) + code.ljust(512, b'\0') + data.ljust(512, b'\0')


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {}
    for alignment in range(3):
        script = b' '*alignment + b'Add-MpPreference -ExclusionPath $p\nreagentc /disable\n'
        cases[f'encoded-{alignment}.exe'] = (pe(data=base64.b64encode(script)), {D, R}, set())
    cases.update({
        'admin-query.exe': (pe(data=base64.b64encode(
            b'Get-MpPreference\nreagentc /enable')), set(), {D, R}),
        'encoded-data-section.exe': (pe(data=base64.b64encode(
            b'Add-MpPreference -ExclusionPath $p\nreagentc /disable'),
            data_name='.data'), set(), {D, R}),
        'token-profile.exe': (pe(TOKEN, APIS), {T}, set()),
        'token-names-only.exe': (pe(data=APIS), set(), {T}),
        'token-other-target.exe': (pe(TOKEN, APIS.replace(b'lsass.exe', b'other.exe')), set(), {T}),
        'token-other-access.exe': (pe(TOKEN.replace(bytes.fromhex('FF 01 0F 00'),
                                                   bytes.fromhex('08 00 00 00')), APIS), set(), {T}),
        'token-data-section.exe': (pe(data=TOKEN+APIS), set(), {T}),
        'rename-delete.exe': (pe(RENAME+DELETE), {N, X}, set()),
        'other-info-class.exe': (pe(RENAME.replace(b'\x04\x03\0\0\0',
                                                  b'\x04\x05\0\0\0')), set(), {N}),
        'delete-false.exe': (pe(DELETE.replace(b'\x01\0\0\0', b'\0\0\0\0', 1)), set(), {X}),
        'delete-other-buffer.exe': (pe(DELETE[:25]+b'\xf0\x02\0\0'+DELETE[29:]), set(), {X}),
        'rename-delete-data.exe': (pe(data=RENAME+DELETE), set(), {N, X}),
    })
    for name, (content, _, _) in cases.items():
        (dest/name).write_bytes(content)
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
        str(ROOT), '--format', 'json', str(dest)], check=True, text=True,
        capture_output=True)
    docs, rest = [], result.stdout.strip()
    decoder = json.JSONDecoder()
    while rest:
        doc, end = decoder.raw_decode(rest)
        docs.append(doc)
        rest = rest[end:].lstrip()
    reports = {Path(f['path']).name: f for d in docs for f in d.get('files', [d])}
    for name, (_, present, absent) in cases.items():
        traits = {t['id']: t for t in reports[name]['traits']}
        assert present <= traits.keys(), (name, 'missing', present-traits.keys())
        assert not absent & traits.keys(), (name, 'unexpected', absent & traits.keys())
        assert not any(t['crit'] == 5 for t in traits.values()), (name, 'hostile')
    print(f'{len(cases)} positive and near-miss controls passed')


if __name__ == '__main__':
    main()
