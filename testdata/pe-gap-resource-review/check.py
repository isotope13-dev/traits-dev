"""Check opcode relationships against an original PE and nonexecuted mutations.

Usage: python3 check.py ORIGINAL --evidence-dir SCRATCH
Artifacts stay in the supplied scratch directory; no specimen is committed.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[2]
GAP = 'objectives/anti-static/obfuscation/control-flow/poly::x86-mixed-width-host-gap-decoder'
LOAD = 'objectives/execution/payload/native-call::x86-host-gap-decoder-native-stage'
DECODE = 'objectives/anti-static/obfuscation/payload/polymorphic/decryptor::x86-resource-delta-unrolled-decoder'
GRAFT = 'objectives/impact/infect/binary/graft::duplicated-resource-arithmetic-body-graft'
FOCUS = {GAP, LOAD, DECODE, GRAFT}

parser = argparse.ArgumentParser()
parser.add_argument('original', type=Path)
parser.add_argument('--evidence-dir', type=Path, required=True)
args = parser.parse_args()
args.evidence_dir.mkdir(parents=True, exist_ok=True)
data = args.original.read_bytes()
nt = struct.unpack_from('<I', data, 60)[0]
opt_size = struct.unpack_from('<H', data, nt+20)[0]
count = struct.unpack_from('<H', data, nt+6)[0]
sections = []
for i in range(count):
    h = nt+24+opt_size+i*40
    name = data[h:h+8].rstrip(b'\0')
    vsize, rva, size, offset = struct.unpack_from('<4I', data, h+8)
    sections.append((name, rva, offset, size, h))
def raw(rva):
    return next(offset+rva-start for _, start, offset, size, _ in sections if start <= rva < start+size)

cases = {'original': (bytearray(data), FOCUS)}
keys = bytearray(data)
# Change immediate keys in both decoders, preserving their relationships.
keys[raw(0x1116)] ^= 0x5a
keys[raw(0x1324)] ^= 0x35
keys[raw(0x48f01f)] ^= 0x7b
cases['changed-keys'] = (keys, FOCUS)
no_byte = bytearray(data)
no_byte[raw(0x1111)] = 0x90
cases['missing-byte-decoder'] = (no_byte, {DECODE, GRAFT})
no_call = bytearray(data)
assert no_call[raw(0x41a2):raw(0x41a2)+2] == b'\xff\xd7'
no_call[raw(0x41a2)+1] = 0xe7
cases['offset-jump-without-call'] = (no_call, {GAP, DECODE, GRAFT})
no_stub = bytearray(data)
stub_off = raw(0x48f000)
no_stub[stub_off] = 0x90
cases['missing-resource-decoder'] = (no_stub, {GAP, LOAD})
wrong_section = bytearray(no_stub)
# The same bytes in a code section cannot establish a resource decoder.
wrong_section[raw(0x5000):raw(0x5000)+80] = data[stub_off:stub_off+80]
cases['decoder-outside-resources'] = (wrong_section, {GAP, LOAD})
low_entropy = bytearray(data)
_, _, offset, size, _ = sections[-1]
low_entropy[offset:offset+size] = bytes(size)
low_entropy[stub_off:stub_off+80] = data[stub_off:stub_off+80]
cases['plain-resource-with-decoder'] = (low_entropy, {GAP, LOAD, DECODE})
paths = []
for label, (content, _) in cases.items():
    p = args.evidence_dir/(label+'.exe')
    p.write_bytes(content)
    paths.append(str(p))
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json', *paths], capture_output=True, text=True, check=True)
(args.evidence_dir/'controls.jsonl').write_text(result.stdout)
assert not result.stderr.strip(), result.stderr
observed = {}
for line in result.stdout.split('\n'):
    if not line.strip():
        continue
    report = json.loads(line)
    for f in report['files']:
        label = Path(f['path']).stem
        if label not in cases:
            continue
        ids = {t['id'] for t in f.get('traits', [])} & FOCUS
        assert ids == cases[label][1], (label, ids, cases[label][1])
        observed[label] = sorted(ids)
assert set(observed) == set(cases), set(observed)
(args.evidence_dir/'results.json').write_text(json.dumps(observed, indent=2)+'\n')
print('PASS: seven PE controls; changed keys retain detection; missing relationships reject')

# Nonexecuting shifted-header controls exercise the actual PNG/COFF relation.
MASK = 'objectives/anti-static/obfuscation/payload/malformed::png-magic-shifted-pe32-header'
png_paths = []
for label, header, machine, magic, expected in [
    ('masked-header', 0x80, 0x14c, b'\x89PNG\r\n\x1a\n', True),
    ('shifted-masked-header', 0x180, 0x14c, b'\x89PNG\r\n\x1a\n', True),
    ('wrong-machine', 0x80, 0, b'\x89PNG\r\n\x1a\n', False),
    ('missing-image-magic', 0x80, 0x14c, bytes(8), False),
]:
    content = bytearray(1024)
    content[:8] = magic
    struct.pack_into('<I', content, 8, header)
    struct.pack_into('<HH', content, header+4, machine, 3)
    struct.pack_into('<H', content, header+20, 0xe0)
    struct.pack_into('<H', content, header+24, 0x10b)
    struct.pack_into('<I', content, header+56, 0x1000)
    content[header+248:header+256] = b'.text\0\0\0'
    p = args.evidence_dir/(label+'.bin')
    p.write_bytes(content)
    png_paths.append((str(p), expected))
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json', *[p for p, _ in png_paths]], capture_output=True, text=True, check=True)
assert not result.stderr.strip(), result.stderr
(args.evidence_dir/'header-controls.jsonl').write_text(result.stdout)
seen = set()
for line in result.stdout.split('\n'):
    if not line.strip():
        continue
    for f in json.loads(line)['files']:
        expected = dict(png_paths).get(f['path'])
        if expected is None:
            continue
        assert (MASK in {t['id'] for t in f.get('traits', [])}) == expected, f['path']
        seen.add(f['path'])
assert seen == set(dict(png_paths))
print('PASS: four shifted-header controls; different offsets match; missing COFF/image evidence rejects')
