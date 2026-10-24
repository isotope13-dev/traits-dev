#!/usr/bin/env python3
"""Read saved JSONL to check relocated observations and retained attack coverage.
Usage: check.py /path/to/controls.final.jsonl /path/to/batch.after.jsonl
Never executes a sample.
"""
import json
from pathlib import Path
import sys

def files(path):
    return [f for line in Path(path).read_text().splitlines()
            for f in json.loads(line).get('raw', json.loads(line)).get('files', [])]

def ids(f):
    return {t['id'] for t in f['traits']}

controls = {Path(f['path']).name: f for f in files(sys.argv[1])}
enc = 'micro-behaviors/data/encoding/xor::'
crypto = {'micro-behaviors/crypto/encrypt::gost28147-encrypt-helper-call',
          'micro-behaviors/crypto/decrypt::aes-cbc-decrypt-helper-call',
          'micro-behaviors/crypto/decrypt::threefish-decrypt-helper-call'}
assert crypto <= ids(controls['crypto-calls.py'])
assert not crypto & ids(controls['declarations-only.c'])
assert enc+'python-xor-bytes-literal-key' in ids(controls['xor-key-material.py'])
assert 'metadata/lang/source/syntax/call/arguments::bytes-literal-xor-argument-text' in ids(controls['xor-key-material.py'])
assert not any(t['crit'] >= 4 for t in controls['xor-key-material.py']['traits'])
assert enc+'python-xor-bytes-literal-key' not in ids(controls['xor-near-miss.py'])
assert 'metadata/lang/source/syntax/call/arguments::bytes-literal-xor-argument-text' in ids(controls['xor-scalar-length.py'])
assert enc+'python-xor-bytes-literal-key' not in ids(controls['xor-scalar-length.py'])
assert 'objectives/anti-static/obfuscation/eval/scripting/decode::xor-layered-python-packer' in ids(controls['xor-loader.py'])
assert 'objectives/execution/payload/file-exec::zone-cleared-decoded-zip-forfiles' in ids(controls['launcher.py'])
assert 'objectives/evasion/process/injection/memory::dynamic-resolution-download-decrypt-stage' in ids(controls['wininet-cng-dynamic-resolution-stager.dll'])
assert not any(t['crit'] >= 4 for t in controls['zstd-decompress.exe']['traits'])
for f in files(sys.argv[2]):
    names = ids(f)
    if f['type'] in ('c', 'python'):
        assert crypto <= names
        assert 'micro-behaviors/mem/protect/modify::heap-page-allocator-protect-pages-call' in names
        assert 'micro-behaviors/fs/path/metadata-store::wmi-repository-objects-data-path' in names
        assert not any(t['crit'] >= 4 for t in f['traits'])
    elif f['type'] == 'pe':
        assert 'objectives/execution/payload/file-exec::xor-record-http-file-launch-code' in names
        assert 'well-known/malware/backdoor/blihan::blihan-command-loader' in names
        assert sum(t['crit'] == 5 for t in f['traits']) >= 2
        assert 'objectives/command-and-control/dropper/staging/native/payload::wininet-embedded-pe-dynamic-stager' not in names
print('PASS: source boundaries, existing attacks, and both PE analysis units')

if len(sys.argv) > 3:
    f = files(sys.argv[3])[0]
    trait = next(t for t in f['traits'] if t['id'] == 'micro-behaviors/communications/http/client/wininet::unsigned-wininet-embedded-header-api-profile')
    assert trait['crit'] == 3
    assert not any(t['crit'] == 5 for t in f['traits'])
    print('PASS: inert WinInet/header co-occurrence is notable')
