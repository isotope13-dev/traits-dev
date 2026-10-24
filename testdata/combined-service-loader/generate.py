"""Inert PE fixtures for serialized loader roles and opaque-data near misses."""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).parent


def pe(data):
    b = bytearray(1536 + ((len(data) + 511) // 512) * 512)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 60, 128)
    b[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 132, 0x8664, 2, 0, 0, 0, 240, 0x22)
    o = 152
    struct.pack_into('<H', b, o, 0x20b)
    struct.pack_into('<I', b, o + 16, 4096)
    struct.pack_into('<Q', b, o + 24, 0x140000000)
    struct.pack_into('<II', b, o + 32, 4096, 512)
    struct.pack_into('<II', b, o + 56, 0x10000, 1024)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<I', b, o + 108, 16)
    for j, (name, rva, pa, size, flags) in enumerate([
        (b'.text', 4096, 1024, 512, 0x60000020),
        (b'.rdata', 8192, 1536, len(b) - 1536, 0x40000040),
    ]):
        q = o + 240 + j * 40
        b[q:q + len(name)] = name
        struct.pack_into('<IIII', b, q + 8, size, rva, size, pa)
        struct.pack_into('<I', b, q + 36, flags)
    b[1024] = 0xc3
    b[1536:1536 + len(data)] = data
    return b


parts = {
    'aes': b'aAES\0aCounter\0anew\0aMODE_CTR\0acounter\0adecrypt\0',
    'base85': b'ab85decode\0azlib\0adecompress\0',
    'hidden': b'aPopen\0aCREATE_NO_WINDOW\0T\2acreationflags\0',
    'decrypt': b'u[+] Background decryption started\0',
    'write': b'u[+] Payload written: \0',
    'analysis': b'u[-] VM detected - legit only\0',
    'remote': b'aVirtualAllocEx\0aWriteProcessMemory\0aCreateRemoteThread\0',
}
cases = []
for omit in [None, *parts]:
    name = ('positive' if omit is None else 'without-' + omit) + '.exe'
    data = b'NUITKA_ONEFILE_PARENT\0' + b'\0'.join(v for k, v in parts.items() if k != omit)
    (ROOT / name).write_bytes(pe(data))
    # These fixtures contain serialized names and status strings but no
    # executable decoder/launcher path; marker co-occurrence is not behavior.
    cases.append(dict(case_id=name, path=str(ROOT / name), matched=[], not_matched=[]))

name = 'opaque-encoded-near-misses.exe'
(ROOT / name).write_bytes(pe(b'\0uX!udpX!tcpX!ntpX!vseX@##@X_raw_cpuid_X^DBOGUS{2X\0Timer\0'))
cases.append(dict(case_id=name, path=str(ROOT / name), matched=[], not_matched=[
    'objectives/command-and-control/backdoor/rat/tasking::c2-multi-vector-command-set',
    'objectives/command-and-control/backdoor/tasking/delimited::twostroke-command-field-delimiter',
    'well-known/lib/platform/raw-cpuid::rust-raw-cpuid-lib',
    'micro-behaviors/data/format/crypto-address::doge-address-regex',
    'micro-behaviors/time/schedule/keywords::dotnet-timer-with-winforms-reference',
]))
name = 'complete-command-table.exe'
(ROOT / name).write_bytes(pe(b'\0!udp\0!tcp\0!ntp\0!vse\0'))
cases.append(dict(case_id=name, path=str(ROOT / name), matched=[
    'objectives/command-and-control/backdoor/rat/tasking::c2-multi-vector-command-set',
], not_matched=[]))
name = 'dogecoin-pattern-controls.js'
(ROOT / name).write_text('const dogecoin = /^D[5-9A-HJ-NP-U][1-9A-HJ-NP-Za-km-z]{25,34}$/;\n')
cases.append(dict(case_id=name, path=str(ROOT / name), matched=[
    'micro-behaviors/data/format/crypto-address::doge-address-regex',
], not_matched=[]))
(ROOT / 'cases.json').write_text(json.dumps({'id_map': {}, 'fixtures': cases}, indent=2) + '\n')
