"""Static positive and near-miss controls; fixtures are never executed."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def pe_fixture(code, imports=()):
    """Minimal inert x64 PE with declared imports and configurable code bytes."""
    b = bytearray(0x2a00)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x8664, 2, 0, 0, 0, 0xf0, 0x22)
    o = 0x98
    struct.pack_into('<H', b, o, 0x20b)
    struct.pack_into('<I', b, o+4, 0x2000)
    struct.pack_into('<IIQ', b, o+16, 0x1000, 0x1000, 0x140000000)
    struct.pack_into('<II', b, o+32, 0x1000, 0x200)
    struct.pack_into('<HH', b, o+40, 6, 0)
    struct.pack_into('<II', b, o+56, 0x4000, 0x200)
    struct.pack_into('<HH', b, o+68, 2, 0x140)
    struct.pack_into('<QQQQ', b, o+72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<I', b, o+108, 16)
    for off, name, va, raw, size, flags in [
        (o+0xf0, b'.text', 0x1000, 0x200, 0x2000, 0x60000020),
        (o+0xf0+40, b'.rdata', 0x3000, 0x2200, 0x800, 0x40000040),
    ]:
        struct.pack_into('<8sIIIIIIHHI', b, off, name, size, va, size, raw, 0, 0, 0, 0, flags)
    b[0x200:0x2200] = b'\x90' * 0x2000
    b[0x200:0x200+len(code)] = code
    if imports:
        struct.pack_into('<II', b, o+112+8, 0x3000, (len(imports)+1)*20)
        cursor = (len(imports)+1)*20
        for index, (library, names) in enumerate(imports):
            dll = cursor
            value = library.encode()+b'\0'
            b[0x2200+cursor:0x2200+cursor+len(value)] = value
            cursor += len(value)
            cursor = (cursor+7)&~7
            ilt = cursor
            cursor += 8*(len(names)+1)
            iat = cursor
            cursor += 8*(len(names)+1)
            for n, name in enumerate(names):
                hint = cursor
                value = b'\0\0'+name.encode()+b'\0'
                b[0x2200+cursor:0x2200+cursor+len(value)] = value
                cursor += len(value)
                struct.pack_into('<Q', b, 0x2200+ilt+8*n, 0x3000+hint)
                struct.pack_into('<Q', b, 0x2200+iat+8*n, 0x3000+hint)
            struct.pack_into('<IIIII', b, 0x2200+20*index, 0x3000+ilt, 0, 0, 0x3000+dll, 0x3000+iat)
        assert cursor < 0x800
    return bytes(b)

def scan(path):
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', str(path),
    ], capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    traits = [t for f in report['files'] for t in f.get('traits', [])]
    return {t['id'] for t in traits}, [t['id'] for t in traits if t['crit'] == 5]

cases = json.loads((HERE/'cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='encrypted-native-controls-') as temp:
    temp = Path(temp)
    parser = bytes.fromhex('65 48 8B 04 25 60 00 00 00 48 63 40 3C B8 4D 5A 00 00')
    loop = bytes.fromhex('45 69 C0 03 00 01 00 41 C1 C8 0D 45 33 C1')
    hook = bytes.fromhex('45 33 C9 48 8D 15 00 00 00 00 4C 8B C0 41 8D 49 0D FF 15 00 00 00 00 C3')
    hook_import = [('USER32.dll', ['SetWindowsHookExA'])]
    fixtures = {
        'hash-loop-near.exe': pe_fixture(parser+loop+b'\xc3'),
        'hash-loop-far.exe': pe_fixture(parser+b'\x90'*5000+loop+b'\xc3'),
        'ordinary-multiply.exe': pe_fixture(parser+bytes.fromhex('6B C0 21 C3')),
        'keyboard-type13.exe': pe_fixture(hook, hook_import),
        'mouse-type14.exe': pe_fixture(hook.replace(b'\x49\x0d', b'\x49\x0e'), hook_import),
        'resource-api-client.exe': pe_fixture(b'\xc3', [
            ('KERNEL32.dll', ['FindResourceA', 'LoadResource', 'LockResource', 'SizeofResource', 'GetThreadContext', 'SetThreadContext', 'ResumeThread', 'VirtualProtect']),
            ('USER32.dll', ['SetWindowsHookExA']),
            ('WININET.dll', ['InternetReadFile', 'InternetOpenW', 'HttpOpenRequestW']),
            ('SHELL32.dll', ['ShellExecuteExA']),
        ]),
    }
    for name, value in fixtures.items():
        (temp/name).write_bytes(value)
    for case in cases:
        path = temp/case['path'] if case['path'].endswith('.exe') else HERE/case['path']
        matched, hostile = scan(path)
        assert set(case['matched']) <= matched, (path.name, set(case['matched'])-matched)
        assert not set(case['not_matched']) & matched, (path.name, set(case['not_matched']) & matched)
        assert not hostile, (path.name, hostile)
        print(path.name, 'PASS')
