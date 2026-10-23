#!/usr/bin/env python3
"""Regression boundaries for the final three coverage gaps; never execute samples."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--inventory', required=True)
p.add_argument('--members', required=True)
p.add_argument('--output', required=True)
p.add_argument('--atomscan', default='../scan/target/release/atomscan')
a = p.parse_args()
samples = json.loads(Path(a.inventory).read_text())['samples']
def sample(prefix):
    row = next(x for x in samples if x['sha256'].startswith(prefix))
    data = Path(row['local_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    return data

def patch(data, needle, replacement):
    assert needle in data, needle
    assert len(needle) == len(replacement)
    return data.replace(needle, replacement)

def at_rva(data, rva):
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    count, size = struct.unpack_from('<H', data, pe+6)[0], struct.unpack_from('<H', data, pe+20)[0]
    for i in range(count):
        virtual, rawsize, raw = struct.unpack_from('<III', data, pe+24+size+40*i+12)
        if virtual <= rva < virtual+rawsize:
            return raw+rva-virtual
    raise AssertionError(hex(rva))

replica = 'objectives/impact/infect/virus::self-mutating-image-submission-loop'
inject = 'objectives/evasion/process/injection/runtime::tls-flattened-remote-image-injection'
disguise = 'objectives/evasion/masquerade/version-resource/claim::remote-client-storage-utility-disguise'
cases = []
with tempfile.TemporaryDirectory(prefix='triage-coverage-') as directory:
    directory = Path(directory)
    def add(name, data, yes=(), no=(), ceiling=None):
        path = directory/name
        path.write_bytes(data)
        cases.append((path, set(yes), set(no), ceiling))
    data = sample('aab86')
    add('replicator.exe', data, (replica,))
    renamed = patch(data, b'rifaien yanje', b'changed title')
    renamed = re.sub(rb'http://[^\x00\s]+', lambda m: b'http://'+b'x'*(len(m[0])-7), renamed)
    add('replicator-renamed-infrastructure.exe', renamed, (replica,))
    add('replicator-no-self-read.exe', patch(data, b'GetModuleFileNameA', b'GetModuleFileNameX'), no=(replica,))
    add('replicator-no-random-source.exe', patch(data, b'rand\x00', b'xxxx\x00'), no=(replica,))
    altered = bytearray(data)
    altered[at_rva(data, 0x153d)+13] ^= 8
    add('replicator-different-mutation-buffer.exe', altered, no=(replica,))
    altered = bytearray(data)
    at = at_rva(data, 0x1638)+30
    assert altered[at] == 0xe8
    altered[at+1:at+5] = b'\0'*4
    add('replicator-no-submit-call.exe', altered, no=(replica,))
    altered = bytearray(data)
    at = at_rva(data, 0x169e)
    altered[at+26:at+30] = b'\0'*4
    altered[at+47:at+51] = b'\0'*4
    add('replicator-no-repeat.exe', altered, no=(replica,))

    data = sample('49e0')
    add('flattened-loader.exe', data, (inject,))
    add('loader-no-rwx-allocation.exe', patch(data, bytes.fromhex('c7442420400000004c8bac24'), bytes.fromhex('c7442420040000004c8bac24')), no=(inject,))
    altered = bytearray(data)
    at = at_rva(data, 0x9627)+16
    altered[at] ^= 8
    add('loader-different-process-slot.exe', altered, no=(inject,))
    altered = bytearray(data)
    at = at_rva(data, 0xc71d)
    assert altered[at:at+3] == bytes.fromhex('ff9424')
    altered[at:at+7] = b'\x90'*7
    add('loader-no-remote-thread.exe', altered, no=(inject,))
    altered, count = re.subn(rb'\x65([\x48\x4c]\x8b.\x25\x58\x00\x00\x00)', lambda m: b'\x64'+m[1], data, flags=re.S)
    assert count >= 5
    add('loader-no-tls-dispatch.exe', altered, no=(inject,))

    data = Path(a.members, 'DISKMGR.exe').read_bytes()
    assert hashlib.sha256(data).hexdigest() == 'bf41e6af51ccba343098f403093b195fb5f238559f723d4088196a2648fb9272'
    add('disguised-remote-client.exe', data, (disguise,))
    add('honest-remote-client.exe', patch(data, 'Disk Manager Tool'.encode('utf-16le'), 'Remote Admin Tool'.encode('utf-16le')), no=(disguise,))
    add('storage-claim-no-remote-identity.exe', patch(data, 'RdClient\\uCrypto.pas'.encode('utf-16le'), 'NoClient\\uCrypto.pas'.encode('utf-16le')), no=(disguise,))
    add('genuine-service.exe', Path(a.members, 'RDSERVICE.exe').read_bytes(), no=(disguise,), ceiling=3)
    add('packed-wrapper.exe', sample('b9115'), (disguise,))

    scan = subprocess.run([a.atomscan, '--no-update', '--mode', 'slow', '--format', 'json', 'path'] + [str(x[0]) for x in cases], env=dict(os.environ, CLEAVE_TRAITS_DIR=str(Path.cwd())), capture_output=True, text=True)
    assert scan.returncode in (0, 1), scan.stderr
    found = {}
    for line in scan.stdout.splitlines():
        files = json.loads(line)['raw']['files']
        found[files[0]['path']] = files
    assert len(found) == len(cases), (len(found), len(cases), scan.stderr)
    result = []
    for path, yes, no, ceiling in cases:
        files = found[str(path)]
        traits = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
        assert all(traits.get(key) == 5 for key in yes), (path.name, yes, {k:v for k,v in traits.items() if v>=4})
        assert not no.intersection(traits), (path.name, no.intersection(traits))
        if ceiling is not None:
            assert max(traits.values(), default=0) <= ceiling, (path.name, traits)
        if path.name == 'packed-wrapper.exe':
            assert {f['sha'] for f in files} >= {'bf41e6af51ccba343098f403093b195fb5f238559f723d4088196a2648fb9272', '7ed2a077a1ce34fcb182e5135ae75ad7bd96207c3204c9f343095f967bfa109f'}
            assert any(t['id'] == disguise and t['crit'] == 5 for t in files[0]['traits']), 'wrapper must retain child hostile evidence'
        result.append({'case': path.name, 'required_hostile': sorted(yes), 'forbidden': sorted(no), 'max_criticality': ceiling, 'passed': True})
    Path(a.output).write_text(json.dumps(result, indent=2)+'\n')
    print(f'{len(result)} final coverage boundary cases passed')
