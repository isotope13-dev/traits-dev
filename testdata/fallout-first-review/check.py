#!/usr/bin/env python3
"""Check behavior boundaries against original, non-executed PE fixtures."""
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parents[2]
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
vm = 'objectives/anti-analysis/vm-detect/wmi::managed-vm-test-wmi-failfast-references'
kill = 'objectives/anti-analysis/tool-detect/process::managed-debugger-kill-process-references'
xor = 'micro-behaviors/data/decode/xor::cil-modulo-key-byte-xor-sequence'
screen = 'objectives/collection/screenshot::managed-credential-collector-png-screen-capture'
write = 'micro-behaviors/data/decode/xor::x86-xor-pe-buffer-write-arguments'
hexrun = 'metadata/file/encoding::perl-hex-escape-run'
base = 'micro-behaviors/data/buffer/carve::perl-nop-hex-buffer'
context = 'micro-behaviors/data/buffer/carve::perl-nop-hex-buffer-output-context'
checks = []

def fixture(name, data, present=(), absent=()):
    path = out / name
    path.write_bytes(data)
    checks.append((path, set(present), set(absent)))

stealer = lzma.decompress((repo / 'testdata/hostile/review-phemedrone.exe.xz').read_bytes())
worm = lzma.decompress((repo / 'testdata/hostile/review-pstore-drive-worm.exe.xz').read_bytes())
assert hashlib.sha256(stealer).hexdigest() == 'f1a261a2786add315b3de022a05766ee1fd72a21931a66701599701f6a9c6844'
assert hashlib.sha256(worm).hexdigest() == '5af839fcc76a5aeb984469190543ca27e2d70c1841f6cc98c9feee6b27d8a972'
fixture('renamed-managed.exe', stealer, [vm, kill, xor, screen])
fixture('renamed-native.exe', worm, [write])
for name, old, new, absent in [
    ('no-vm.exe', b'<IsVM>b__', b'<Test>b__', vm),
    ('no-killer.exe', b'<KillDebuggers>b__', b'<ListProcesses>b__', kill),
    ('no-xor.exe', bytes.fromhex('61 d1 fe 0e 04 00'), bytes.fromhex('58 d1 fe 0e 04 00'), xor),
    ('no-capture.exe', b'CopyFromScreen', b'CopyFromBuffer', screen),
]:
    assert old in stealer and len(old) == len(new)
    fixture(name, stealer.replace(old, new), absent=[absent])
for name, offset in [('wrong-size.exe', 0x29159), ('wrong-buffer.exe', 0x2915e)]:
    data = bytearray(worm)
    data[offset] ^= 1
    fixture(name, data, absent=[write])
for name in ['dotnet-default-manifest.dll', 'managed-status-stubs-only.exe']:
    checks.append((repo / 'testdata/benign' / name, set(), {vm, kill, xor, screen, write}))
for name, present in [('crlf_benign.pl', False), ('split_positive.pl', True), ('long_positive.pl', True)]:
    checks.append((repo / 'testdata/perl-hex-run-precision' / name,
                   {hexrun} if present else set(), set() if present else {hexrun}))
perl = (repo / 'testdata/benign/perl-shellcode-file-generator-controls.pl').read_bytes()
fixture('renamed-buffer.pl', perl, [hexrun, base, context])
fixture('no-nops.pl', perl.replace(b'"\\x90" x 28', b'"A" x 28'), [hexrun], [base, context])
fixture('no-output.pl', perl.replace(b'print $fh $buff . $nop . $shell;', b''), [hexrun, base], [context])
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
                         '--format', 'json', *[str(p) for p, _, _ in checks]],
                        capture_output=True, text=True, check=True)
# The CLI may concatenate report objects without a line separator.
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for entry in report['files']:
        files[str(Path(entry['path']).resolve())] = entry
for path, present, absent in checks:
    entry = files[str(path.resolve())]
    got = {t['id'] for t in entry['traits']}
    assert present <= got, (path.name, 'missing', present - got)
    assert not absent & got, (path.name, 'unexpected', absent & got)
print(f'{len(checks)} behavior-boundary controls passed')
