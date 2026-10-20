#!/usr/bin/env python3
"""Focused binary controls; usage: check.py MANAGED_SAMPLE NATIVE_SAMPLE."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

managed = Path(sys.argv[1]).read_bytes()
native = Path(sys.argv[2]).read_bytes()
assert hashlib.sha256(managed).hexdigest() == 'c215e2e0512237d2428926071a0c78f4c20f838903a05fd05441f3a785b1ed29'
assert hashlib.sha256(native).hexdigest() == '9e89865032e1c045c73e67f3018d6001c54999f9a4a4ef364953e60a5dec5c71'
repo = Path(__file__).resolve().parents[3]
append_id = 'micro-behaviors/fs/write/file/append::managed-append-random-buffer-profile'
ip_id = 'micro-behaviors/communications/ip/literal::external-ipv4-shaped-text-binary'
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp)
    original = bytes.fromhex('1c 18 73 dd 00 00 0a')
    pos = managed.index(original, 0x5a18, 0x5a18 + 250)
    for name, replacement in [
        ('open-mode', bytes.fromhex('19 18 73 dd 00 00 0a')),
        ('changed-tokens', bytes.fromhex('1c 18 73 de 00 00 0a')),
    ]:
        data = bytearray(managed)
        data[pos:pos + len(original)] = replacement
        (out / (name + '.exe')).write_bytes(data)
    for name, old, new in [
        ('no-nextbytes', b'NextBytes\0', b'OtherCall\0'),
        ('no-filestream', b'FileStream\0', b'OtherClass\0'),
    ]:
        assert managed.count(old) == 1
        (out / (name + '.exe')).write_bytes(managed.replace(old, new))
    pos = native.index(b'3.8.10.2')
    for name, replacement in [
        ('public-ip', b'45.77.12.34'),
        ('private-ip', b'10.0.0.1'),
        ('invalid-ip', b'999.0.0.1'),
    ]:
        data = bytearray(native)
        data[pos:pos + 15] = b'\0' * 15
        data[pos:pos + len(replacement)] = replacement
        (out / (name + '.exe')).write_bytes(data)
    result = subprocess.run(
        ['cleave', '--traits-dir', str(repo), '--format', 'json', str(out)],
        check=True, capture_output=True, text=True,
    )
    remaining = result.stdout.strip()
    decoder = json.JSONDecoder()
    findings = {}
    while remaining:
        document, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in document['files']:
            findings[Path(file['path']).stem] = {t['id'] for t in file['traits']}
    for name, trait, expected in [
        ('changed-tokens', append_id, True),
        ('open-mode', append_id, False),
        ('no-nextbytes', append_id, False),
        ('no-filestream', append_id, False),
        ('public-ip', ip_id, True),
        ('private-ip', ip_id, False),
        ('invalid-ip', ip_id, False),
    ]:
        assert (trait in findings[name]) == expected, name
        print(name + ': PASS')
