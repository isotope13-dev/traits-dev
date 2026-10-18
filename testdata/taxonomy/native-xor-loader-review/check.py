"""Generate inert PE controls and check source/sink and API-only boundaries."""
import json
import random
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DECODE = bytes.fromhex(
    '0f b6 32 33 c9 8b ff 8b c6 33 c1 3c eb 75 14 '
    '0f b6 42 01 33 c1 3c 02 75 0a 0f b6 42 03 33 c1 3c f1 74 0f '
    '41 81 f9 00 01 00 00 72 db 5e 5f 33 c0 5d c3 33 c0 85 ed 76 09 '
    '30 0c 10 40 3b 47 14 72 f7')
EXEC = bytes.fromhex(
    '6a 40 68 00 30 00 00 40 50 6a 00 89 7d f8 ff 15 00 20 40 00 '
    '89 45 fc 85 c0 74 3f 8b 0e 8b 57 10 51 52 50 e8 00 00 00 00 '
    '83 c4 0c 90 8b 5d fc 53 5e 90 ff d6')
XOR = 'micro-behaviors/data/decode/xor::x86-header-key-search-byte-xor'
CALL = 'micro-behaviors/process/deploy::x86-rwx-copied-buffer-call'
LOADER = 'objectives/anti-static/obfuscation/encoding/xor::x86-key-searched-xor-code-loader'
HTTP = 'micro-behaviors/communications/http/client/wininet::unsigned-rwx-reloc-wininet-api-profile'
MAPPING = 'micro-behaviors/communications/http/client/wininet::unsigned-reloc-wininet-file-mapping-api-profile'
TEMP = 'micro-behaviors/fs/path/temp::word-style-temp-filename'
OLD = {
    'objectives/command-and-control/dropper/staging/native/loader::unsigned-rwx-reloc-wininet-stage-loader',
    'objectives/command-and-control/dropper/staging/native/loader::unsigned-reloc-wininet-mapped-download-stub',
}


def image(decoder=b'', execution=b'', executable=True):
    rng = random.Random(1729)
    data = bytearray(rng.getrandbits(8) for _ in range(0x13400))
    data[:0x400] = bytes(0x400)
    def put(off, fmt, *args):
        struct.pack_into('<' + fmt, data, off, *args)
    data[:2] = b'MZ'
    put(0x3c, 'I', 0x80)
    data[0x80:0x84] = b'PE\0\0'
    put(0x84, 'HHIIIHH', 0x14c, 3, 1700000000, 0, 0, 224, 0x102)
    opt = 0x98
    put(opt, 'H', 0x10b)
    for off, val in {4:0x2000, 8:0x11000, 16:0x1000, 20:0x1000,
                     24:0x3000, 28:0x400000, 32:0x1000, 36:0x200,
                     56:0x14000, 60:0x400, 92:16}.items():
        put(opt + off, 'I', val)
    put(opt + 40, 'HH', 4, 0)
    put(opt + 68, 'H', 3)
    put(opt + 104, 'II', 0x3000, 60)
    for i, (name, size, va, raw, flags) in enumerate([
        (b'.text', 0x2000, 0x1000, 0x400, 0xe0000020 if executable else 0xc0000040),
        (b'.rdata', 0x1000, 0x3000, 0x2400, 0x40000040),
        (b'.reloc', 0x10000, 0x4000, 0x3400, 0xe0000040),
    ]):
        put(opt + 224 + 40*i, '8sIIIIIIHHI', name, size, va, size, raw, 0, 0, 0, 0, flags)
    # Entry returns; all signature fragments are unreachable static controls.
    data[0x400] = 0xc3
    data[0x500:0x500 + len(decoder)] = decoder
    data[0x700:0x700 + len(execution)] = execution
    data[0x2400:0x3400] = bytes(0x1000)
    names = [('KERNEL32.dll', ['VirtualAlloc', 'MapViewOfFile', 'GetProcAddress', 'IsDebuggerPresent']),
             ('WININET.dll', ['InternetOpenW', 'InternetConnectW', 'HttpOpenRequestW',
                              'HttpSendRequestW', 'InternetReadFile', 'HttpQueryInfoW'])]
    cursor = 0x2900
    for i, (dll, apis) in enumerate(names):
        dllpos = 0x2480 + i*0x30
        data[dllpos:dllpos+len(dll)+1] = dll.encode() + b'\0'
        ilt, iat = 0x2500+i*0x80, 0x2700+i*0x80
        rva = lambda pos: pos + 0xc00
        put(0x2400+i*20, 'IIIII', rva(ilt), 0, 0, rva(dllpos), rva(iat))
        for j, api in enumerate(apis):
            data[cursor:cursor+len(api)+3] = b'\0\0'+api.encode()+b'\0'
            put(ilt+4*j, 'I', rva(cursor))
            put(iat+4*j, 'I', rva(cursor))
            cursor += len(api)+3
    temp = '~WRD1234.tmp\0'.encode('utf-16le')
    data[0x3100:0x3100+len(temp)] = temp
    return data


def main():
    cases = [
        ('both', DECODE, EXEC, {XOR, CALL, LOADER}, set()),
        ('decoder-only', DECODE, b'', {XOR}, {CALL, LOADER}),
        ('execution-only', b'', EXEC, {CALL}, {XOR, LOADER}),
        ('changed-xor-operation', DECODE.replace(b'\x30\x0c\x10', b'\x88\x0c\x10'), EXEC,
         {CALL}, {XOR, LOADER}),
        ('wrong-saved-execution-pointer', DECODE, EXEC.replace(b'\x8b\x5d\xfc', b'\x8b\x5d\xf4'),
         {XOR}, {CALL, LOADER}),
        ('api-layout-only', b'', b'', set(), {XOR, CALL, LOADER}),
    ]
    with tempfile.TemporaryDirectory() as td:
        for name, decoder, execution, present, absent in cases:
            path = Path(td)/(name+'.exe')
            path.write_bytes(image(decoder, execution))
            run = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json',
                                  'analyze', str(path)], capture_output=True, text=True)
            if not run.stdout.strip():
                raise RuntimeError(run.stderr)
            report = json.loads(run.stdout)
            traits = {t['id']: t for f in report['files'] for t in f['traits']}
            assert present <= traits.keys(), (name, present-traits.keys())
            assert not (absent | OLD) & traits.keys(), (name, (absent | OLD) & traits.keys())
            if name == 'api-layout-only':
                assert not any(t['crit'] >= 4 for t in traits.values()), name
            for key in [HTTP, MAPPING, TEMP]:
                assert traits[key]['crit'] == 3, (name, key, traits.get(key))
            print(name, 'PASS')

if __name__ == '__main__':
    main()
