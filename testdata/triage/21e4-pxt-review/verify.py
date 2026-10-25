#!/usr/bin/env python3
"""Generate byte-derived gate controls and XML permission near misses; scan once.

Usage: python3 verify.py <Vyholeg.bat.decoded> <scratch-output-directory>
Does not execute the sample. Requires cleave and dnfile.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import dnfile

sample, output = map(Path, sys.argv[1:])
original = sample.read_bytes()
assert hashlib.sha256(original).hexdigest() == '21e4abb7a38009a70335679ea874f774c12dc47d7794d8a1e1515d6f3f6ea7b9'
output.mkdir(parents=True, exist_ok=True)
controls = output / 'controls'
controls.mkdir(exist_ok=True)
gate = 'objectives/anti-analysis/debugger-detect/combined-checks::managed-debugger-delegate-exit-layout'
network = 'metadata/permission/network::appx-internet-client'
storage = 'metadata/permission/storage::appx-removable-storage'
expected = {}
def save(name, data, required=(), forbidden=()):
    (controls / name).write_bytes(data)
    expected[name] = {'required': list(required), 'forbidden': list(forbidden)}

save('original.exe', original, [gate])
# Change method RIDs and local indices while retaining the same control layout.
p = dnfile.dnPE(data=original)
code = p.get_offset_from_rva(p.net.mdtables.MethodDef.rows[2].Rva)
# CIL offsets include the 12-byte fat method header.
start = code + 0xa4
assert original[start:start+7].hex() == '280c00000a2d0d'
variant = bytearray(original)
variant[start+1:start+4] = b'\x3c\x00\x00'
variant[start+8] = 7
variant[start+12] = 8
save('different-rids-and-locals.exe', variant, [gate])
# Branches must skip exactly the exit block; an unconditional branch does not
# show the debugger-dependent short circuit, and a removed call cannot exit.
for name, offset, replacement in [
    ('no-conditional-debugger-gate.exe', start+5, b'\x2b'),
    ('no-exit-call.exe', code+0xb9, b'\x00'*5),
    ('wrong-branch-target.exe', start+6, b'\x01'),
]:
    data = bytearray(original)
    data[offset:offset+len(replacement)] = replacement
    save(name, data, forbidden=[gate])
assert original.count(b'\x00get_IsAttached\x00') == 1
save('no-debugger-name.exe', original.replace(b'\x00get_IsAttached\x00', b'\x00get_IsDetached\x00'), forbidden=[gate])

prefix = '<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10" xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"><Capabilities>'
suffix = '</Capabilities></Package>'
def xml(name, body, required=(), forbidden=()):
    save(name, (prefix+body+suffix).encode(), required, forbidden)
xml('permissions.xml', '<Capability Name="internetClient"/><uap:Capability Name="removableStorage"/>', [network, storage])
xml('multiline-single-quotes.xml', "<Capability\nName = 'internetClient'/><uap:Capability Name = 'removableStorage'/>", [network, storage])
# Standard Capability schema has Name as its sole attribute. Namespaced spelling
# and whitespace are accepted; another attribute containing Name text is not.
xml('namespaced-storage.xml', "<uap:Capability Name = 'removableStorage' xmlns:uap='urn:uap'/>", [storage], [network])
xml('comments.xml', '<!-- <Capability Name="internetClient"/><Capability Name="removableStorage"/> -->', forbidden=[network, storage])
xml('similar-names.xml', '<Capability Name="internetClientServer"/><Capability Name="removableStorageOther"/>', forbidden=[network, storage])
xml('attribute-text.xml', '<Capability Description="Name=\'internetClient\'"/><Capability Description="Name=\'removableStorage\'"/>', forbidden=[network, storage])
xml('different-element.xml', '<NotCapability Name="internetClient"/><DeviceCapability Name="removableStorage"/>', forbidden=[network, storage])

r = subprocess.run(['cleave', '--all-files', '--format', 'json', str(controls)], check=True, capture_output=True, text=True)
(output/'controls.scan.json').write_text(r.stdout)
(output/'controls.scan.log').write_text(r.stderr)
reports = []
remaining = r.stdout.lstrip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])} for d in reports for f in d['files']}
results = []
for name, checks in expected.items():
    got = files[name]
    assert set(checks['required']) <= got, (name, 'missing', set(checks['required'])-got)
    assert not set(checks['forbidden']) & got, (name, 'unexpected', set(checks['forbidden'])&got)
    results.append({'name': name, **checks, 'passed': True})
(output/'controls.results.json').write_text(json.dumps(results, indent=2)+'\n')
print(f'{len(results)} controls passed')
