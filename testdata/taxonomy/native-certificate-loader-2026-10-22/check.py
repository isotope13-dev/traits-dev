#!/usr/bin/env python3
"""Static dependency-removal controls; never execute the input binaries.
Usage: check.py <extracted-wincorlib.dll> <extracted-host.exe> <scratch-dir>
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
ENGINE = os.environ.get('CLEAVE', 'cleave')
RC4 = 'micro-behaviors/crypto/symmetric/stream/rc4::x64-stack-byte-wrapped-prga'
RX = 'micro-behaviors/process/inject/runtime/call::x64-security-directory-rx-buffer-call'
HASH = 'micro-behaviors/os/api-resolution/hash-based::x64-ror13-name-ordinal-export-walk'
CERT = 'objectives/anti-static/obfuscation/steganography/signature::rc4-security-table-code-loader'
SLEEP = 'objectives/evasion/process/hook/inline::peb-host-entry-infinite-sleep-trampoline-x64'
DISGUISE = 'objectives/evasion/process/hook/inline::unsigned-microsoft-dll-host-entry-sleep-hijack'
TRAIL = 'metadata/signed/certificate/signature::pe-authenticode-unsigned-trailing-data'
ALL = {RC4, RX, HASH, CERT, SLEEP, DISGUISE, TRAIL}


def scan(path):
    result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                            capture_output=True, text=True, check=True)
    doc = json.loads(result.stdout)
    return {t['id'] for f in doc['files'] for t in f.get('traits', [])}


def replace_once(data, old, new):
    assert data.count(old) == 1, (old.hex(), data.count(old))
    assert len(old) == len(new)
    return data.replace(old, new)


def main():
    dll, host, scratch = map(Path, sys.argv[1:])
    scratch.mkdir(parents=True, exist_ok=True)
    original = dll.read_bytes()
    cases = [('renamed-companion.exe', original, ALL - {TRAIL})]
    cases.append(('without-rc4-buffer-xor.exe', replace_once(original,
        bytes.fromhex('300b48ffc34983eb0175c5'),
        bytes.fromhex('880b48ffc34983eb0175c5')),
        {RX, HASH, SLEEP, DISGUISE}))
    cases.append(('without-security-directory-read.exe', replace_once(original,
        bytes.fromhex('8b9404f80000008bb404fc000000'),
        bytes.fromhex('8b9404f00000008bb404f4000000')),
        {RC4, HASH, SLEEP, DISGUISE}))
    cases.append(('finite-sleep-trampoline.exe', replace_once(original,
        bytes.fromhex('c74609ffffffff'), bytes.fromhex('c74609e8030000')),
        {RC4, RX, HASH, CERT}))
    cases.append(('without-microsoft-claim.exe', original.replace(
        'Microsoft Corporation'.encode('utf-16le'),
        'Xicrosoft Corporation'.encode('utf-16le')),
        {RC4, RX, HASH, CERT, SLEEP}))
    cases.append(('renamed-section.exe', replace_once(original, b'.iqe6bn\0', b'.extra\0\0'),
                  ALL - {TRAIL}))
    original_host = host.read_bytes()
    cases.append(('signed-carrier.exe', original_host, {TRAIL}))
    # Reconstruct a comparison carrier with the unsigned certificate suffix
    # removed. This is a control, not a claim to have recovered an original.
    nt = struct.unpack_from('<I', original_host, 0x3c)[0]
    directory = nt + 24 + 112 + 4 * 8
    cert_offset, _ = struct.unpack_from('<II', original_host, directory)
    marker = original_host.index(bytes.fromhex('cafebabe'), cert_offset)
    clean = bytearray(original_host[:marker])
    struct.pack_into('<I', clean, directory + 4, marker - cert_offset)
    struct.pack_into('<I', clean, cert_offset, marker - cert_offset)
    cases.append(('carrier-without-unsigned-suffix.exe', clean, set()))
    for name, data, expected in cases:
        path = scratch / name
        path.write_bytes(data)
        actual = scan(path) & ALL
        assert actual == expected, (name, expected, actual)
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
