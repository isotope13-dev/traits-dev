"""Check resource placement and process-query coverage without running a sample.

Pass the reviewed assembly with --sample and a writable --scratch-dir.
dnfile is used only to locate its managed resource. Mutated assemblies are
static measurement controls, not runnable application variants.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess

import dnfile

parser = argparse.ArgumentParser()
parser.add_argument('--sample', type=Path, required=True)
parser.add_argument('--scratch-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
args.scratch_dir.mkdir(parents=True, exist_ok=True)
original = args.sample.read_bytes()
pe = dnfile.dnPE(data=original)
resource = max(pe.net.resources, key=lambda r: r.size)
assert resource.size >= 65536
offset = pe.get_offset_from_rva(resource.rva)
assert original[offset:offset + resource.size] == resource.data
assert struct.unpack_from('<I', original, offset - 4)[0] == resource.size

large = 'metadata/binary/resource/size::clr-resource-large'
entropy = 'metadata/binary/resource/entropy::clr-resource-high-entropy'
combined = 'metadata/binary/resource/entropy::clr-resource-size-and-entropy'
wql = 'micro-behaviors/process/enumerate/wmi::win32-process-wql-enumeration'
by_id = 'micro-behaviors/process/info/query::dotnet-get-process-by-id-member'
invoke_member = 'micro-behaviors/metaprogramming/reflection::invoke-member-token'
retired = {
    'micro-behaviors/process/enumerate/managed::dotnet-get-process-by-id-member',
    'micro-behaviors/process/interpreter/reflection/runtime::invoke-member-token',
    'metadata/binary/resource/identity::clr-resource-large',
    'metadata/binary/resource/size::clr-resource-high-entropy',
    'metadata/binary/resource/size::dotnet-large-high-entropy-managed-resource',
}


def modified_resource(size, data):
    image = bytearray(original)
    struct.pack_into('<I', image, offset - 4, size)
    image[offset:offset + resource.size] = data.ljust(resource.size, b'\0')
    return bytes(image)


def inert_pe(strings):
    """A RET entry point and non-executed UTF-16 query text."""
    payload = b'\xc3\0' + '\0'.join(strings).encode('utf-16le') + b'\0\0'
    raw_size = (len(payload) + 511) & ~511
    image = bytearray(512 + raw_size)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', image, optional, 0x10b)
    for position, value in {4: raw_size, 16: 0x1000, 20: 0x1000,
                            28: 0x400000, 32: 0x1000, 36: 512,
                            56: 0x2000, 60: 512, 92: 16}.items():
        struct.pack_into('<I', image, optional + position, value)
    struct.pack_into('<H', image, optional + 68, 3)
    struct.pack_into('<8sIIIIIIHHI', image, optional + 224, b'.text',
                     len(payload), 0x1000, raw_size, 512, 0, 0, 0, 0, 0x60000020)
    image[512:512 + len(payload)] = payload
    return bytes(image)


cases = [
    ('reviewed.exe', original, {large, entropy, combined, wql, by_id, invoke_member}, set()),
    ('without-invoke-member.exe',
     original.replace(b'InvokeMember', b'InvokeMembex'),
     {by_id}, {invoke_member}),
    ('pid-lookup-without-enumeration.exe',
     original.replace('Win32_Process'.encode('utf-16le'),
                      'Win32_Procesx'.encode('utf-16le')),
     {by_id, invoke_member}, {wql}),
    ('large-zero-resource.exe', modified_resource(resource.size, b''),
     {large}, {entropy, combined}),
    ('small-entropy-resource.exe', modified_resource(4096, resource.data[:4096]),
     {entropy}, {large, combined}),
    ('small-zero-resource.exe', modified_resource(4096, b''),
     set(), {large, entropy, combined}),
    ('projected-process-query.exe', inert_pe([
        "SELECT ProcessId, CommandLine FROM Win32_Process WHERE Name='editor.exe'"
    ]), {wql}, {by_id}),
    ('all-process-query.dll', inert_pe(['select * from win32_process']),
     {wql}, {by_id}),
    ('different-wmi-class.exe', inert_pe(['SELECT * FROM Win32_Processor']),
     set(), {wql, by_id}),
    ('class-name-only.exe', inert_pe(['Win32_Process', 'GetProcessById']),
     set(), {wql, by_id}),
    ('native-method-name.exe', inert_pe(['GetProcessById']),
     set(), {wql, by_id}),
]
for name, content, _, _ in cases:
    (args.scratch_dir / name).write_bytes(content)
result = subprocess.run(
    [args.cleave, '--traits-dir', str(repo), '--format', 'json',
     *[str(args.scratch_dir / name) for name, _, _, _ in cases]],
    capture_output=True, text=True, check=True)
reports = {}
remaining = result.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.update({Path(f['path']).name: f for f in report['files']})
    remaining = remaining[end:].lstrip()
for name, _, required, forbidden in cases:
    traits = {t['id']: t for t in reports[name]['traits']}
    assert required <= traits.keys(), (name, 'missing', required - traits.keys())
    assert not (forbidden | retired) & traits.keys(), (name, 'unexpected',
                                                         (forbidden | retired) & traits.keys())
    for tid in required:
        assert traits[tid]['crit'] == 3, (name, tid, traits[tid]['crit'])
    if name == 'pid-lookup-without-enumeration.exe':
        assert not [tid for tid in traits if tid.startswith(
            'micro-behaviors/process/enumerate/')], name
    if name == 'reviewed.exe':
        assert not [t for t in traits.values() if t['crit'] >= 4], name
    print('PASS', name)
