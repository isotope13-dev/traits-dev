"""Exercise interop memory versus API lookup, and address versus adapter names.

The generated PE files contain inert string tables, never executable samples.
Pass an output directory explicitly to keep generated files outside the tree.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--directory', required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
out = Path(args.directory).resolve()
out.mkdir(parents=True, exist_ok=True)
alloc = 'micro-behaviors/mem/alloc/heap::dotnet-unmanaged-allocation-name'
uni = 'micro-behaviors/mem/alloc/heap::dotnet-unicode-string-allocation'
read = 'micro-behaviors/mem/read/arbitrary::dotnet-ansi-pointer-string-read'
free = 'micro-behaviors/mem/free::dotnet-unmanaged-free-name'
adapter = 'micro-behaviors/network/interface::loopback-adapter-name'
retired = {
    'micro-behaviors/os/api-resolution/dynamic::managed-unmanaged-memory-marshalling',
    'micro-behaviors/os/api-resolution/dynamic::managed-unicode-marshalling',
    'micro-behaviors/os/api-resolution/dynamic::managed-ansi-marshalling',
    'micro-behaviors/os/sysinfo/network::loopback-adapter-name',
}
cases = [
    ('interop', ['AllocHGlobal', 'StringToHGlobalUni', 'PtrToStringAnsi', 'FreeHGlobal'], {alloc, uni, read, free}, {adapter}),
    ('com-interop', ['AllocCoTaskMem', 'FreeCoTaskMem'], {alloc, free}, {uni, read, adapter}),
    ('reallocation', ['ReAllocHGlobal', 'ReAllocCoTaskMem'], set(), {alloc, uni, read, free}),
    ('address', ['System.Net', 'IPAddress', 'Loopback'], set(), {adapter}),
    ('adapter', ['Loopback Pseudo-Interface 1'], {adapter}, {alloc, uni, read, free}),
    ('address-and-adapter', ['IPAddress', 'Loopback', 'Loopback Adapter'], {adapter}, {alloc, uni, read, free}),
    ('lookup', ['GetProcAddress', 'LoadLibraryW'], set(), {alloc, uni, read, free, adapter}),
]

def pe_strings(strings):
    data = bytearray(1024)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', data, optional, 0x10b)
    struct.pack_into('<III', data, optional + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', data, optional + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', data, optional + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, optional + 68, 3)
    struct.pack_into('<I', data, optional + 92, 16)
    section = optional + 224
    struct.pack_into('<8sIIIIIIHHI', data, section, b'.text', 512, 0x1000, 512, 512, 0, 0, 0, 0, 0x60000020)
    payload = b'\0'.join(s.encode() for s in strings) + b'\0'
    data[512:512 + len(payload)] = payload
    return data

paths = []
for name, strings, _, _ in cases:
    path = out / (name + '.exe')
    path.write_bytes(pe_strings(strings))
    paths.append(str(path))
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', *paths], capture_output=True, text=True, check=True)
remaining = result.stdout.strip()
reports = []
decoder = json.JSONDecoder()
while remaining:
    report, pos = decoder.raw_decode(remaining)
    reports.extend(report['files'])
    remaining = remaining[pos:].lstrip()
by_name = {Path(f['path']).stem: f for f in reports}
for name, _, required, forbidden in cases:
    traits = {t['id']: t for t in by_name[name]['traits']}
    assert required <= traits.keys(), (name, 'missing', required - traits.keys())
    assert not (forbidden | retired) & traits.keys(), (name, 'unexpected', (forbidden | retired) & traits.keys())
    for tid in required:
        assert traits[tid]['crit'] == 3, (name, tid, traits[tid]['crit'])
    print('PASS', name)
