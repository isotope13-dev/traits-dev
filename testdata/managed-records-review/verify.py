"""Static matcher controls; generated PE stubs return immediately.

Run: python3 testdata/managed-records-review/verify.py <scratch-directory>
The marker tables model required evidence, not observed runtime behavior.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SCREEN = 'objectives/collection/screenshot::managed-screen-recording'
KEYLOG = 'objectives/collection/keylog/hook::dotnet-hook-keylog-recording'
XOR = 'micro-behaviors/crypto/symmetric/xor/loop::cil-modulo-key-byte-array-xor'
CAPTURE = 'micro-behaviors/hardware/display/screenshot::dotnet-copyfromscreen-capture'
RETIRED = {
    'objectives/collection/screenshot::dotnet-socket-screenshot-registry-rat',
    'objectives/exfiltration/stealer/input::dotnet-hook-keylogger-network-exfil',
}
CAPTURE_MARKERS = ['CopyFromScreen', 'get_PrimaryScreen', 'get_Jpeg',
                   'NetworkStream', 'RegistryKey', 'SetValue', 'ToBase64String']
KEYLOG_MARKERS = ['Append', 'WH_KEYBOARD_LL', 'SetWindowsHookEx',
                  'UnhookWindowsHookEx', 'CallNextHookEx', 'Keylogger', 'KEYLOG:']
CIL_XOR = bytes.fromhex(
    '8f 10 00 00 01 25 71 10 00 00 01 07 08 07 8e 69 5d 91 61 d2 81 10 00 00 01 '
    '08 17 58 0c 08 06 8e 69 fe 04 13 06 11 06 2d d5')


def build_pe(markers, cil=b''):
    text = bytearray(0x1000)
    text[:3] = b'\x33\xc0\xc3'
    # CLI header and a metadata version root, with no runnable managed entry.
    struct.pack_into('<IHHIIII', text, 0x10, 72, 2, 5, 0x1080, 32, 1, 0)
    root = b'BSJB' + struct.pack('<HHII', 1, 1, 0, 12) + b'v4.0.30319\x00\x00'
    text[0x80:0x80 + len(root)] = root
    text[0x100:0x100 + len(cil)] = cil
    table = b'\x00'.join(s.encode() for s in markers) + b'\x00'
    text[0x200:0x200 + len(table)] = table
    header = bytearray(0x200)
    header[:2] = b'MZ'
    struct.pack_into('<I', header, 0x3c, 0x80)
    header[0x80:0x84] = b'PE\x00\x00'
    struct.pack_into('<HHIIIHH', header, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', header, opt, 0x10b)
    struct.pack_into('<III', header, opt + 4, 0x1000, 0, 0)
    struct.pack_into('<III', header, opt + 16, 0x1000, 0x1000, 0x1000)
    struct.pack_into('<III', header, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', header, opt + 40, 4, 0)
    struct.pack_into('<II', header, opt + 56, 0x3000, 0x200)
    struct.pack_into('<H', header, opt + 68, 3)
    struct.pack_into('<I', header, opt + 92, 16)
    struct.pack_into('<II', header, opt + 96 + 14 * 8, 0x1010, 72)
    sec = opt + 224
    header[sec:sec + 8] = b'.text\x00\x00\x00'
    struct.pack_into('<IIIIIIHHI', header, sec + 8,
                     0x1000, 0x1000, 0x1000, 0x200, 0, 0, 0, 0, 0x60000020)
    return header + text


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = [
        ('capture-network-registry.exe', CAPTURE_MARKERS, b'', False, False),
        ('screen-label-without-keylog.exe', CAPTURE_MARKERS + ['SCREENSHOT:'], b'', False, False),
        ('screen-record.exe', CAPTURE_MARKERS + KEYLOG_MARKERS + ['SCREEN:'], b'', True, False),
        ('screenshot-record.exe', CAPTURE_MARKERS + KEYLOG_MARKERS + ['SCREENSHOT:'], b'', True, False),
        ('keylog-without-screen-record.exe', CAPTURE_MARKERS + KEYLOG_MARKERS, b'', False, False),
        ('modulo-xor.exe', [], CIL_XOR, False, True),
        ('modulo-or.exe', [], CIL_XOR.replace(b'\x91\x61\xd2', b'\x91\x60\xd2'), False, False),
        ('add-index-xor.exe', [], CIL_XOR.replace(b'\x69\x5d\x91', b'\x69\x58\x91'), False, False),
        ('xor-without-loop.exe', [], CIL_XOR[:25], False, False),
    ]
    for name, markers, cil, screen, xor in cases:
        path = dest / name
        path.write_bytes(build_pe(markers, cil))
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--disable', 'third-party', '--format', 'json', str(path)],
            capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f['traits']}
        assert (SCREEN in traits) == screen, (name, 'screen', sorted(traits))
        assert (XOR in traits) == xor, (name, 'xor', sorted(traits))
        assert not RETIRED.intersection(traits), name
        if not screen and KEYLOG not in traits:
            assert not any(t['crit'] == 5 for t in traits.values()), name
        if KEYLOG_MARKERS[0] in markers:
            assert KEYLOG in traits, name
        if 'CopyFromScreen' in markers:
            assert traits[CAPTURE]['crit'] == 3, (name, traits[CAPTURE])
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
