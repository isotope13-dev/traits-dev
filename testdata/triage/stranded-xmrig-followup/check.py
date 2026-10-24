"""Inert controls for kernel capabilities and placement; never execute a PE.

Usage: python3 check.py OUT [TRAITS_DIR]
TRAITS_DIR optionally permits comparison against an earlier rule revision.
"""
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
TRAITS = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT
pe = runpy.run_path(str(ROOT / 'testdata/taxonomy/pe-review-boundaries/check.py'))['pe']
MB = 'micro-behaviors/'
READ = MB + 'os/kernel/driver::x64-io-port-read-to-buffer'
WRITE = MB + 'os/kernel/driver::x64-io-port-write-from-buffer'
HAL_READ = MB + 'os/kernel/driver::hal-bus-config-read'
HAL_WRITE = MB + 'os/kernel/driver::hal-bus-config-write'
MAP = MB + 'mem/map::mm-map-io-space'
UNMAP = MB + 'mem/unmap::mm-unmap-io-space'
GROUP = MB + 'mem/combined::kernel-io-space-map-or-unmap'
LEGACY_GROUP = MB + 'mem/combined::virtual-allocation-or-page-protection'
EXIT = MB + 'process/thread/terminate::exit-thread'
CREATE = MB + 'process/create/thread::create-thread'
FLS = MB + 'process/tls::fls-with-thread-creation'
rd = bytes.fromhex('66 ED 66 89 01')
wr = bytes.fromhex('0F B7 41 04 66 EF')
cases = {}


def case(name, image, yes=(), no=(), notable=()):
    p = OUT / (name + '.exe')
    p.write_bytes(image)
    cases[str(p)] = (set(yes), set(no), set(notable))


case('port-read-write', pe({}, text=rd + b'\x90' * 8 + wr), [READ, WRITE])
case('port-data-only', pe({}, data=rd + wr), no=[READ, WRITE])
case('port-in-only', pe({}, text=bytes.fromhex('66 ED')), no=[READ, WRITE])
case('port-read-without-store', pe({}, text=rd.replace(b'\x89', b'\x85')), no=[READ])
case('port-write-without-out', pe({}, text=wr[:-1] + b'\x90'), no=[WRITE])
case('port-write-other-displacement', pe({}, text=wr.replace(b'\x04', b'\x18')), [WRITE])
wrong_arch = pe({}, text=rd + wr)
struct.pack_into('<H', wrong_arch, 0x84, 0xAA64)
case('port-other-architecture', wrong_arch, no=[READ, WRITE])
case('hal-imports', pe({'HAL.dll': ['HalGetBusDataByOffset', 'HalSetBusDataByOffset']}),
     [HAL_READ, HAL_WRITE], notable=[HAL_READ, HAL_WRITE])
case('hal-string-mentions', pe({}, data=b'HalGetBusDataByOffset\0HalSetBusDataByOffset\0'),
     no=[HAL_READ, HAL_WRITE])
case('map-import', pe({'ntoskrnl.exe': ['MmMapIoSpace']}), [MAP, GROUP, LEGACY_GROUP], [UNMAP])
case('map-ex-import', pe({'ntoskrnl.exe': ['MmMapIoSpaceEx']}), [MAP, GROUP, LEGACY_GROUP])
case('unmap-import', pe({'ntoskrnl.exe': ['MmUnmapIoSpace']}), [UNMAP], [MAP, GROUP], [UNMAP])
case('map-and-unmap', pe({'ntoskrnl.exe': ['MmMapIoSpace', 'MmUnmapIoSpace']}),
     [MAP, UNMAP, GROUP], notable=[MAP, UNMAP])
for name, token, target, grouped in [
    ('xoradd-unmap', b'yXcYUXJrSnN^', 'mem/unmap::mm-unmap-io-space-xoradd-string', False),
    ('atbash-map', b'NnNzkRlHkzxv', 'mem/map::mm-map-io-space-atbash-string', True),
    ('atbash-unmap', b'NnFmnzkRlHkzxv', 'mem/unmap::mm-unmap-io-space-atbash-string', True),
]:
    case(name, pe({}, data=token + b'\0'), [MB + target, LEGACY_GROUP] + ([GROUP] if grouped else []))
case('map-string-only', pe({}, data=b'MmMapIoSpace\0MmUnmapIoSpace\0'), no=[MAP, UNMAP, GROUP])
case('thread-exit', pe({'KERNEL32.dll': ['ExitThread']}), [EXIT], [CREATE])
case('thread-create', pe({'KERNEL32.dll': ['CreateThread']}), [CREATE], [EXIT])
case('fls-with-exit', pe({'KERNEL32.dll': ['ExitThread', 'FlsAlloc', 'FlsGetValue']}), [EXIT], [FLS])
case('fls-with-create', pe({'KERNEL32.dll': ['CreateThread', 'FlsAlloc', 'FlsGetValue']}), [CREATE, FLS])
KDF = MB + 'crypto/kdf/algorithm::'
case('kdf-references', pe({}, data=b'argon2\0EVP_PKEY_derive\0'),
     [KDF + 'argon2', KDF + 'evp-pkey-derive', KDF + 'key-derivation'],
     notable=[KDF + 'argon2', KDF + 'evp-pkey-derive', KDF + 'key-derivation'])
case('ordinary-strings', pe({}, data=b'hardware monitor\0configuration\0'),
     no=[MAP, UNMAP, GROUP, HAL_READ, HAL_WRITE, READ, WRITE])

r = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(TRAITS),
                    '--format', 'json', *cases], text=True, capture_output=True)
assert r.returncode == 0, r.stderr
(OUT / 'reports.json').write_text(r.stdout)
decoder = json.JSONDecoder()
remaining = r.stdout.lstrip()
reports = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.extend(report['files'])
    remaining = remaining[end:].lstrip()
if len(sys.argv) > 2:
    print(f'Captured baseline: {len(reports)} controls')
else:
    assert len(reports) == len(cases)
    for f in reports:
        yes, no, notable = cases[f['path']]
        traits = {t['id']: t['crit'] for t in f.get('traits', [])}
        hidden = {GROUP, LEGACY_GROUP, EXIT, KDF + 'key-derivation'}
        assert yes - hidden <= traits.keys(), (f['path'], 'missing', yes - hidden - traits.keys())
        assert not no & traits.keys(), (f['path'], 'unexpected', no & traits.keys())
        assert all(traits[t] == 3 for t in notable - hidden), (f['path'], 'not notable', notable)
        assert all(t < 4 for t in traits.values()), (f['path'], 'unwarranted attack inference')
    print(f'PASS: {len(cases)} kernel/memory/thread/crypto controls')
