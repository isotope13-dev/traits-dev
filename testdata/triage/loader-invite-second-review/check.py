#!/usr/bin/env python3
"""Static matcher controls; specimen bytes stay in the supplied scratch path."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KEY = 'objectives/collection/keylog/polling::native-xor-key-recording'
ENC = 'micro-behaviors/data/encode/xor::x86-xor-copy-write-handoff'
PROFILE = 'micro-behaviors/fs/enumerate/drives::logical-drive-file-api-profile'
WORM = 'objectives/lateral-movement/usb-worm/drive-infector::logical-drive-copy-worm'
SFX = 'objectives/command-and-control/dropper/delivery/sfx::sfx-exe-member-name'
PHISH = 'objectives/credential-access/phishing/html-brand::'
CARCHIVE = 'metadata/binary/layout/overlay::carchive-overlay-exe-record'


def api_control():
    """Minimal PE containing ordinary drive/file API imports, no replication."""
    b = bytearray(0x2400)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    o = 0x98
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<III', b, o + 16, 0x1000, 0x1000, 0x1000)
    struct.pack_into('<III', b, o + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', b, o + 56, 0x3000, 0x400)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<I', b, o + 92, 16)
    struct.pack_into('<II', b, o + 104, 0x1100, 40)
    sh = o + 224
    b[sh:sh+8] = b'.rdata\0\0'
    struct.pack_into('<IIII', b, sh + 8, 0x2000, 0x1000, 0x2000, 0x400)
    struct.pack_into('<I', b, sh + 36, 0x40000040)
    b[0x400] = 0xc3
    struct.pack_into('<IIIII', b, 0x500, 0x1200, 0, 0, 0x1180, 0x1300)
    b[0x580:0x58d] = b'KERNEL32.dll\0'
    names = ['GetLogicalDriveStringsA', 'FindFirstFileA', 'FindNextFileA',
             'FindClose', 'GetDriveTypeA', 'DeviceIoControl', 'GetDiskFreeSpaceExA',
             'CreateProcessA']
    pos = 0x800
    for n, name in enumerate(names):
        struct.pack_into('<I', b, 0x600 + 4*n, pos + 0xc00)
        struct.pack_into('<I', b, 0x700 + 4*n, pos + 0xc00)
        raw = b'\0\0' + name.encode() + b'\0'
        b[pos:pos+len(raw)] = raw
        pos += (len(raw)+1) & ~1
    return bytes(b)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--unpacked', required=True, type=Path)
    ap.add_argument('--html', required=True, type=Path)
    ap.add_argument('--scratch', required=True, type=Path)
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    b = a.unpacked.read_bytes()
    loop = bytes.fromhex('8a140180f2628810404e75f48d4424106a005053ff15a0120c10505755ff1580120c10')
    assert b.count(loop) == 1
    old = bytes.fromhex('8a140180f26288104083ee0175f26a008d4424105055ff15a0120c10505753ff1580120c10')
    def patch_code(needle, replacement):
        assert b.count(needle) == 1
        offset = b.index(needle)
        return b[:offset] + replacement + b[offset+len(replacement):]

    cases = [
        ('renamed.dll', b, {KEY, ENC}, {WORM, SFX}),
        ('different-key.dll', b.replace(loop, loop[:5]+b'\x37'+loop[6:]), {KEY, ENC}, set()),
        ('zero-key.dll', b.replace(loop, loop[:5]+b'\0'+loop[6:]), set(), {KEY, ENC}),
        ('other-output.dll', b.replace(loop, loop[:27]+b'\x56'+loop[28:]), set(), {KEY, ENC}),
        ('no-poll.dll', b.replace(b'GetAsyncKeyState', b'GetAsyncRowState'), {ENC}, {KEY}),
        ('no-label.dll', b.replace(b'<Enter>\r\n\0', b'<Other>\r\n\0'), {ENC}, {KEY}),
        ('word-mask.dll', patch_code(bytes.fromhex('560fbff8ff15e8130c10f6c480'),
                                   bytes.fromhex('560fbff8ff15e8130c10b9008000006685c1')), {KEY, ENC}, set()),
        ('sub-decrement.dll', patch_code(loop, old), {KEY, ENC}, set()),
        ('drive-manager.exe', api_control(), {PROFILE}, {WORM, KEY, SFX}),
        ('exe-overlay.exe', api_control()+b'\0\0zagent.exe\0', set(), {CARCHIVE}),
        ('carchive-overlay.exe', api_control()+b'\0\0zagent.exe\0MEI\x0c\x0b\x0a\x0b\x0e', {CARCHIVE}, set()),
        ('invite.html', a.html.read_bytes(), set(), set()),
        ('ordinary-login.html', b'<html><button onclick="location.href=\'login.php\'">Login</button></html>', set(), set()),
    ]
    for name, data, _, _ in cases:
        (a.scratch / name).write_bytes(data)
    cmd = ['cleave', '--traits-dir', str(ROOT), '--no-update-check',
           '--disable', 'third-party,radare2,upx', '--format', 'json']
    cmd.extend(str(a.scratch / name) for name, _, _, _ in cases)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    (a.scratch / 'reports.json').write_text(proc.stdout)
    reports = []
    stream = proc.stdout.lstrip()
    decoder = json.JSONDecoder()
    while stream:
        record, end = decoder.raw_decode(stream)
        reports.extend(record.get('files', [record]))
        stream = stream[end:].lstrip()
    result = []
    for name, _, want, reject in cases:
        path = str(a.scratch / name)
        f = next(f for f in reports if f['path'] == path)
        ts = {t['id']: t for t in f.get('traits', [])}
        assert not (want-ts.keys()), (name, 'missing', want-ts.keys())
        assert not (reject & ts.keys()), (name, 'unexpected', reject & ts.keys())
        if name.endswith('.html') or name == 'drive-manager.exe':
            assert not any(t['crit'] >= 4 for t in ts.values()), (name, 'non-neutral findings')
        assert not any(t.startswith(PHISH) for t in ts), (name, 'unsupported phishing')
        result.append({'case': name, 'required': sorted(want), 'absent': sorted(reject)})
    (a.scratch / 'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
