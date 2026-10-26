"""Inert PE controls: a debug checksum label is not a hashing implementation.

Usage: python3 check.py SCRATCH_DIR
Only static scans run; generated PE entry points contain RET.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import importlib.util
import json
import os
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'pe_controls', ROOT / 'testdata/taxonomy/managed-tuner-observations/check.py')
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)
HASH = 'micro-behaviors/crypto/hash/digest::sha256-code-name-reference'
DEBUG = 'metadata/binary/debug::pe-pdb-sha256-checksum'


def fixture(code=b'', *, debug=True, record_type=19, record_size=39,
            pointer=0x2b0, algorithm=b'SHA256\0'):
    data = bytearray(controls.pe(code))
    if debug:
        # IMAGE_DEBUG_DIRECTORY in .text, plus a 7-byte algorithm name
        # and 32-byte checksum. No runtime code invokes this metadata.
        struct.pack_into('<II', data, 0x98 + 96 + 6*8, 0x1080, 28)
        struct.pack_into('<IIHHIIII', data, 0x280, 0, 0, 0, 0,
                         record_type, record_size, 0x10b0, pointer)
        data[0x2b0:0x2b0+39] = algorithm + bytes(39-len(algorithm))
    return bytes(data)


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    cases = [
        ('debug-only', fixture(), {DEBUG}, {HASH}),
        ('debug-and-hash', fixture(b'SHA256\0'), {DEBUG, HASH}, set()),
        ('debug-and-provider', fixture(b'SHA256Managed\0'), {DEBUG, HASH}, set()),
        ('debug-and-wide-hash', fixture('SHA256\0'.encode('utf-16le')),
         {DEBUG, HASH}, set()),
        ('hash-without-debug', fixture(b'SHA256\0', debug=False), {HASH}, {DEBUG}),
        ('provider-without-debug', fixture(b'SHA256CryptoServiceProvider\0', debug=False),
         {HASH}, {DEBUG}),
        ('hash-prefix-near-miss', fixture(b'SHA256Example\0'), {DEBUG}, {HASH}),
        ('hash-suffix-near-miss', fixture(b'ExampleSHA256\0'), {DEBUG}, {HASH}),
        ('wrong-debug-type', fixture(record_type=2), {HASH}, {DEBUG}),
        ('wrong-debug-size', fixture(record_size=7), {HASH}, {DEBUG}),
        ('wrong-debug-pointer', fixture(pointer=0x2e0), {HASH}, {DEBUG}),
        ('other-checksum', fixture(algorithm=b'SHA384\0'), set(), {DEBUG, HASH}),
    ]

    def check(case):
        name, data, present, absent = case
        path = scratch / (name + '.exe')
        path.write_bytes(data)
        result = subprocess.run([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            'test-rules', str(path), '--rules', HASH + ',' + DEBUG,
        ], capture_output=True, text=True, check=True)
        matched = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.MULTILINE))
        assert present <= matched and not absent & matched, (
            name, present - matched, absent & matched, result.stdout, result.stderr)
        return {'case': name, 'passed': True}

    with ThreadPoolExecutor(max_workers=3) as pool:
        print(json.dumps(list(pool.map(check, cases)), indent=2))


if __name__ == '__main__':
    main()
