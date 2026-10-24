#!/usr/bin/env python3
"""Focused controls; generated PEs test name references, not imported calls."""
import json
import os
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'well-known/malware/trojan/youareanidiot::'
SUSPEND = 'micro-behaviors/process/control/signal::nt-suspend-process-str'
TRANSFORM = 'micro-behaviors/data/encoding/xor::x64-rolling-key-byte-transform'
PACKED = 'objectives/anti-static/pack/section-anomaly::rolling-key-packed-code'
TABLE = 'micro-behaviors/dylib/lookup::native-loader-memory-api-table'
ENTITY = 'micro-behaviors/data/decode/custom::html-angle-entity-substitution'
XOR_THREAD = 'micro-behaviors/process/inject/remote-thread::xor-ntcreatethreadex-name-prefix'
FIELD = 'metadata/lang/source/syntax/member::node-archive-sha256-field'
OLD_FIELD = 'micro-behaviors/crypto/hash/digest::node-archive-sha256-field'

def pe(text=b'\xc3', data=b''):
    buf = bytearray(0x800)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x8664, 2, 0, 0, 0, 0xf0, 0x22)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x20b)
    struct.pack_into('<I', buf, opt + 16, 0x1000)
    struct.pack_into('<Q', buf, opt + 24, 0x140000000)
    struct.pack_into('<II', buf, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', buf, opt + 56, 0x3000, 0x200)
    struct.pack_into('<H', buf, opt + 68, 3)
    struct.pack_into('<I', buf, opt + 108, 16)
    for i, (name, va, raw, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x40000040),
    ]):
        sec = 0x188 + i * 40
        buf[sec:sec + len(name)] = name
        struct.pack_into('<IIII', buf, sec + 8, 0x200, va, 0x200, raw)
        struct.pack_into('<I', buf, sec + 36, flags)
    buf[0x200:0x200 + len(text)] = text
    buf[0x400:0x400 + len(data)] = data
    return bytes(buf)

page = '<script src="arbitrary.js"></script><body onkeydown="altf4key();ctrlkey();delkey();" onmouseout="procreate();">'
refs = b'NtSuspendProcess\0NtResumeProcess\0LdrGetProcedureAddress\0NtAllocateVirtualMemory\0NtProtectVirtualMemory\0RtlMoveMemory\0'
# Change arithmetic keys from the analyzed specimen; behavior stays the same.
transform = bytes.fromhex('0f b6 06 48 81 c6 01 00 00 00 32 c3 34 12 04 34 d0 c0 f6 d0 32 d8')
cases = [
    ('renamed.html', page, {PREFIX + 'legacy-popup-harassment-page'}, set()),
    ('comment.html', '<!--' + page + '-->', set(), {PREFIX + 'legacy-popup-harassment-page'}),
    ('keyboard-only.html', page.replace(' onmouseout="procreate();"', ''), set(), {PREFIX + 'legacy-popup-harassment-page'}),
    ('ordinary.html', '<script src="app.js"></script><body onkeydown="navigate();" onmouseout="dismiss();">', set(), {PREFIX + 'legacy-popup-harassment-page'}),
    ('reference.exe', pe(data=refs), {SUSPEND, TABLE}, {PACKED}),
    ('glued.exe', pe(data=b'AAAA' + refs), {SUSPEND}, {PACKED}),
    ('xor-thread.exe', pe(data=bytes(x ^ 0x23 for x in b'NtCreateThreadE')), {XOR_THREAD}, set()),
    ('xor-thread-other-key.exe', pe(data=bytes(x ^ 0x71 for x in b'NtCreateThreadE')), {XOR_THREAD}, set()),
    ('clear-thread.exe', pe(data=b'NtCreateThreadEx\0'), set(), {XOR_THREAD}),
    ('xor-wrong-section.exe', pe(text=bytes(x ^ 0x23 for x in b'NtCreateThreadE')), set(), {XOR_THREAD}),
    ('suffix.exe', pe(data=b'NtSuspendProcessEx\0'), set(), {SUSPEND}),
    ('transform.exe', pe(text=transform), {TRANSFORM}, {PACKED}),
    ('no-feedback.exe', pe(text=transform[:-2] + b'\x90\x90'), set(), {TRANSFORM, PACKED}),
    ('entities.html', '<script>replaceAll("&amp;lt;", "<", encoded);</script>', {ENTITY}, set()),
    ('entity-comment.html', '<!--<script>replaceAll("&amp;lt;", "<", encoded);</script>-->', set(), {ENTITY}),
    ('archive.js', 'const expected = archive.sha256;', {FIELD}, {OLD_FIELD}),
    ('archive-hash.js', 'const hash = crypto.createHash("sha256"); function actualHash() { return hash.digest("hex"); } if (actualHash() !== archive.sha256) throw Error("mismatch");', {FIELD, 'micro-behaviors/crypto/hash/digest::node-sha256-archive-hash-context'}, {OLD_FIELD}),
    ('no-archive.js', 'const expected = archive.sha512;', set(), {FIELD, OLD_FIELD}),
]
with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
    paths = []
    for name, content, _, _ in cases:
        p = Path(tmp) / name
        p.write_bytes(content.encode() if isinstance(content, str) else content)
        paths.append(str(p))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *paths],
        text=True, capture_output=True, check=True)
    files = []
    remaining = result.stdout.lstrip()
    decoder = json.JSONDecoder()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[end:].lstrip()
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])} for f in files}
    for name, _, required, forbidden in cases:
        ids = found[name]
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
print('18 focused controls passed')
