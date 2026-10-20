"""Offline rule controls. Usage: check.py INFECTED_INSTALLER SCRATCH

Fixtures contain synthetic PE headers, imports and byte-transform snippets.
No sample is executed, and generated binaries remain in SCRATCH.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CONFIG = 'micro-behaviors/os/service/configure::change-service-config2-w-symbol'
ANSI = 'micro-behaviors/os/service/configure::change-service-config2-ansi'
PROFILE = 'micro-behaviors/os/service/configure::service-admin-configure-api-profile'
XOR = 'micro-behaviors/data/encoding/xor::x86-indexed-xor-complement-byte-stores'
OLD = {
    'micro-behaviors/os/service/host::service-config-change',
    'micro-behaviors/os/service/host::change-service-config2-ansi',
    'objectives/persistence/system/service/install::service-admin-import-lifecycle',
}


def pe_fixture(names=(), code=b'\xc3', extra=b''):
    """Minimal x86 PE, with a return stub and optional ADVAPI32 imports."""
    data = bytearray(0xa00)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    for off, value in [(4, 0x200), (8, 0x600), (16, 0x1000),
                       (20, 0x1000), (24, 0x2000), (28, 0x400000),
                       (32, 0x1000), (36, 0x200), (56, 0x3000),
                       (60, 0x200), (72, 0x100000), (76, 0x1000),
                       (80, 0x100000), (84, 0x1000), (92, 16)]:
        struct.pack_into('<I', data, opt + off, value)
    struct.pack_into('<HH', data, opt + 40, 4, 0)
    struct.pack_into('<H', data, opt + 68, 3)
    for i, (name, size, rva, raw, flags) in enumerate([
            (b'.text', 0x200, 0x1000, 0x200, 0x60000020),
            (b'.rdata', 0x600, 0x2000, 0x400, 0x40000040)]):
        struct.pack_into('<8sIIIIIIHHI', data, 0x178 + 40*i,
                         name, size, rva, size, raw, 0, 0, 0, 0, flags)
    data[0x200:0x200+len(code)] = code
    if names:
        struct.pack_into('<II', data, opt + 104, 0x2000, 40)
        struct.pack_into('<IIIII', data, 0x400, 0x2040, 0, 0, 0x2030, 0x2080)
        data[0x430:0x43d] = b'ADVAPI32.dll\0'
        pos = 0x4c0
        for i, name in enumerate(names):
            rva = pos - 0x400 + 0x2000
            struct.pack_into('<I', data, 0x440+4*i, rva)
            struct.pack_into('<I', data, 0x480+4*i, rva)
            value = b'\0\0' + name.encode() + b'\0'
            data[pos:pos+len(value)] = value
            pos = (pos + len(value) + 1) & ~1
    data[0x900:0x900+len(extra)] = extra
    return bytes(data)


def main():
    sample, scratch = map(Path, sys.argv[1:3])
    scratch.mkdir(parents=True, exist_ok=True)
    names = ['OpenSCManagerW', 'OpenServiceW', 'CreateServiceW', 'StartServiceW',
             'ChangeServiceConfig2W', 'DeleteService', 'QueryServiceStatus']
    source = sample.read_bytes()
    loop = source[0x25570:0x255b4]
    assert loop[:2] == b'\x8b\x85' and b'\x33\xc1' in loop and b'\xf7\xd0' in loop
    cases = {
        'service-imports.exe': (pe_fixture(names), {CONFIG, PROFILE}),
        'no-config2.exe': (pe_fixture([n for n in names if n != names[4]]), set()),
        'config2-text-only.exe': (pe_fixture(extra=b'ChangeServiceConfig2W\0'), set()),
        'config2-ansi.exe': (pe_fixture(extra=b'ChangeServiceConfig2A\0'), {ANSI}),
        'no-service-create.exe': (pe_fixture([n for n in names if n != names[2]]), {CONFIG}),
        'transform.exe': (pe_fixture(code=loop+b'\xc3'), {XOR}),
        'no-xor.exe': (pe_fixture(code=loop.replace(b'\x33\xc1', b'\x01\xc1')), set()),
        'no-complement.exe': (pe_fixture(code=loop.replace(b'\xf7\xd0', b'\xf7\xd8')), set()),
        'different-key-slot.exe': (pe_fixture(code=loop.replace(b'\x4d\xf8', b'\x4d\xf4')), {XOR}),
        'transform-in-data.exe': (pe_fixture(extra=loop), set()),
    }
    paths = []
    for name, (data, _) in cases.items():
        path = scratch / name
        path.write_bytes(data)
        paths.append(str(path))
    env = dict(os.environ, CLEAVE_VALIDATE='0')
    proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
                           str(ROOT), '--format', 'json', *paths],
                          env=env, capture_output=True, text=True, check=True)
    (scratch / 'scans.json').write_text(proc.stdout)
    (scratch / 'stderr.txt').write_text(proc.stderr)
    decoder = json.JSONDecoder()
    remaining = proc.stdout.strip()
    observed = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].strip()
        for file in report['files']:
            observed[Path(file['path']).name] = file['traits']
    for name, (_, expected) in cases.items():
        traits = {t['id']: t for t in observed[name]}
        assert not OLD.intersection(traits), name
        assert {CONFIG, ANSI, PROFILE, XOR}.intersection(traits) == expected, name
        assert all(traits[t]['crit'] == 3 for t in expected), name
        # Ordinary service imports alone must not imply unwanted persistence.
        if name == 'service-imports.exe':
            assert not any(t.startswith('objectives/persistence/') for t in traits), traits
    print(f'{len(cases)} controls passed')


if __name__ == '__main__':
    main()
