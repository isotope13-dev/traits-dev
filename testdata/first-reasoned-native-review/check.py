"""Generate inert PE controls and scan them; never execute a specimen.
Usage: python3 testdata/first-reasoned-native-review/check.py <scratch-dir>
"""
import gzip
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
GZIP = 'metadata/binary/layout/overlay::gzip-header-prefix'
AGENT = 'micro-behaviors/data/llm/agent::native-ai-agent-identity'
RWX = 'micro-behaviors/mem/alloc/executable::go-abi-rwx-reserve-commit-call-x64'
PING = 'micro-behaviors/fs/delete/file/command::embedded-ping-delete-command'
ENTRY = 'micro-behaviors/data/arithmetic::go-field-base-sum-call-setup'
OLD = {
    'micro-behaviors/data/embedded/payload/installer::overlay-gzip-magic',
    'objectives/evasion/masquerade/binary/signature::tampered-signed-overlay-execution-stager',
    'objectives/evasion/masquerade/binary/signature::self-issued-digest-mismatch-go-overlay-stager',
}


def pe64(code=b'', data=b'', overlay=b''):
    header = bytearray(512)
    header[:2] = b'MZ'
    struct.pack_into('<I', header, 0x3c, 0x80)
    header[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', header, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', header, opt, 0x20b)
    struct.pack_into('<I', header, opt + 16, 0x1000)
    struct.pack_into('<Q', header, opt + 24, 0x140000000)
    struct.pack_into('<II', header, opt + 32, 4096, 512)
    struct.pack_into('<II', header, opt + 56, 0x3000, 512)
    struct.pack_into('<H', header, opt + 68, 3)
    struct.pack_into('<I', header, opt + 108, 16)
    code = b'\xc3' + code  # entry returns before any test instructions
    for off, name, raw, rva, flags, blob in [
        (0x188, b'.text', 512, 0x1000, 0x60000020, code),
        (0x1b0, b'.rdata', 1024, 0x2000, 0x40000040, data),
    ]:
        struct.pack_into('<8sIIIIIIHHI', header, off, name, max(len(blob), 1),
                         rva, 512, raw, 0, 0, 0, 0, flags)
    assert max(len(code), len(data)) <= 512
    return header + code.ljust(512, b'\0') + data.ljust(512, b'\0') + overlay


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    rwx = bytes.fromhex('B9 00 30 00 00 BF 40 00 00 00 31 F6 45 31 C0 '
                        '45 31 C9 45 31 D2 4D 89 D3 31 C0 E8 00 00 00 00')
    load_field = bytes.fromhex('8B 40 10')
    spill = bytes.fromhex('48 89 84 24 20 00 00 00')
    reload = bytes.fromhex('48 8B 84 24 20 00 00 00')
    load_cx = bytes.fromhex('48 8B 8C 24 28 00 00 00')
    load_dx = bytes.fromhex('48 8B 94 24 30 00 00 00')
    handoff = reload + bytes.fromhex('31 DB 31 C9 48 89 CF E8 00 00 00 00')
    held = load_field + b'\x90' * 10 + load_cx + bytes.fromhex('48 01 C8') + b'\x90' * 5 + spill
    cases = [
        ('bare-short-name', pe64(data=b'Kiro\0'), set(), {AGENT}),
        ('executable-reference', pe64(data=b'Kiro.exe\0'), {AGENT}, set()),
        ('cli-reference', pe64(data=b'kiro-cli\0'), {AGENT}, set()),
        ('four-byte-gzip-collision', pe64(overlay=bytes.fromhex('1f8b0800') + b'noise'), set(), {GZIP}),
        ('gzip-reserved-flags', pe64(overlay=bytes.fromhex('1f8b08e0000000000003')), set(), {GZIP}),
        ('gzip-stream', pe64(overlay=gzip.compress(b'ordinary application data', mtime=0)), {GZIP}, set()),
        ('gzip-loaded-section', pe64(data=gzip.compress(b'ordinary application data', mtime=0)), set(), {GZIP}),
        ('rwx-wrapper-call', pe64(code=rwx), {RWX}, set()),
        ('non-executable-allocation', pe64(code=rwx.replace(bytes.fromhex('BF 40'), bytes.fromhex('BF 04'))), set(), {RWX}),
        ('one-loopback-ping-delete', pe64(data=b'cmd /c ping 127.0.0.1 -n 1&del "%s"\0'), {PING}, set()),
        ('entry-original-cx-dx', pe64(code=load_field + spill + load_cx + load_dx + bytes.fromhex('48 01 D1 48 89 8C 24 20 00 00 00') + handoff), {ENTRY}, set()),
        ('entry-original-ax-cx', pe64(code=load_field + spill + reload + load_cx + bytes.fromhex('48 01 C8') + spill + handoff), {ENTRY}, set()),
        ('entry-register-held', pe64(code=held + handoff), {ENTRY}, set()),
        ('different-structure-field', pe64(code=held.replace(load_field, bytes.fromhex('8B 40 14')) + handoff), set(), {ENTRY}),
        ('without-zero-argument-call', pe64(code=held + reload), set(), {ENTRY}),
    ]
    for name, content, required, absent in cases:
        path = dest / (name + '.exe')
        path.write_bytes(content)
        run = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                             check=True, capture_output=True, text=True)
        report = json.loads(run.stdout)
        findings = [t for f in report['files'] for t in f.get('traits', [])]
        ids = {t['id'] for t in findings}
        assert required <= ids, (name, required - ids)
        assert not (absent | OLD) & ids, (name, (absent | OLD) & ids)
        assert not [t['id'] for t in findings if t['crit'] == 5], name
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
