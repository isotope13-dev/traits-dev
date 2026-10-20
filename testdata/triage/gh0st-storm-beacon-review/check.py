"""PE matcher controls for native data confused with managed APIs/opcodes.

The generated stubs return immediately; embedded bytes model static evidence.
Run with a scratch output directory. No specimen bytes are copied into the repo.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
NAME = 'metadata/binary/symbols/name::delete-value-member-name'
REGISTRY = 'micro-behaviors/os/registry/delete::managed-registry-delete-value-references'
IMUL = 'metadata/binary/instruction/operand::x86-imul-010003c9'
SIDT = 'micro-behaviors/os/sysinfo/hardware::sidt-absolute-destination'
RETIRED = {
    'micro-behaviors/os/registry/manipulate::dotnet-registry-delete-value-member',
    'objectives/anti-static/obfuscation/imports/api-hashing::near-fnv-prime-imul',
    'objectives/persistence/firmware/boot/record::int13-bootkit-loaded-as-kernel-driver',
}


def pe(payload, managed=False):
    header = bytearray(0x200)
    header[:2] = b'MZ'
    struct.pack_into('<I', header, 0x3c, 0x80)
    header[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', header, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', header, opt, 0x10b)
    struct.pack_into('<III', header, opt + 4, 0x1000, 0, 0)
    struct.pack_into('<III', header, opt + 16, 0x1000, 0x1000, 0x1000)
    struct.pack_into('<III', header, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', header, opt + 40, 4, 0)
    struct.pack_into('<II', header, opt + 56, 0x2000, 0x200)
    struct.pack_into('<H', header, opt + 68, 3)
    struct.pack_into('<I', header, opt + 92, 16)
    sec = opt + 224
    header[sec:sec + 8] = b'.text\0\0\0'
    struct.pack_into('<IIIIIIHHI', header, sec + 8,
                     0x1000, 0x1000, 0x1000, 0x200, 0, 0, 0, 0, 0x60000020)
    text = bytearray(0x1000)
    text[:3] = b'\x33\xc0\xc3'
    if managed:
        # Sufficient CLR header/root evidence for the managed-context rules;
        # this is a structural fixture, not a runnable managed program.
        struct.pack_into('<II', header, opt + 96 + 14 * 8, 0x1010, 72)
        struct.pack_into('<IHHIIII', text, 0x10, 72, 2, 5, 0x1080, 32, 1, 0)
        root = b'BSJB' + struct.pack('<HHII', 1, 1, 0, 12) + b'v4.0.30319\0\0'
        text[0x80:0x80 + len(root)] = root
    text[0x200:0x200 + len(payload)] = payload
    return header + text


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    cases = [
        ('bare-member', b'\0DeleteValue\0', False, {NAME}),
        ('native-registry-names', b'\0RegistryKey\0DeleteValue\0', False, {NAME}),
        ('managed-unrelated-member', b'\0DeleteValue\0', True, {NAME}),
        ('managed-registry-references', b'\0RegistryKey\0DeleteValue\0', True, {NAME, REGISTRY}),
        ('numeric-data', bytes.fromhex('43 c9 03 00 4a c9 03 00 4d c9 03 00 01 00'), False, set()),
        ('register-imul', bytes.fromhex('69 c0 c9 03 00 01 c3'), False, {IMUL}),
        ('go-like-pclntab-data', bytes.fromhex('09 2b 0f 01 0d 67 08 02 03 04 03 02'), False, set()),
        ('sidt-store-and-read', bytes.fromhex('0f 01 0d 00 20 40 00 a0 05 20 40 00 c3'), False, {SIDT}),
    ]
    watched = {NAME, REGISTRY, IMUL, SIDT}
    for name, payload, managed, expected in cases:
        path = out / (name + '.exe')
        path.write_bytes(pe(payload, managed))
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--disable', 'third-party', '--format', 'json', str(path)],
            capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f['traits']}
        assert watched.intersection(traits) == expected, (name, watched.intersection(traits))
        assert not RETIRED.intersection(traits), name
        assert not any(t['crit'] >= 4 for t in traits.values()), (name, traits)
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
