#!/usr/bin/env python3
"""Scan inert controls for hostname, bot-protocol and XOR boundaries.

Generated PE entry points are RET, with no active import or network code.
Run from any directory: python3 testdata/taxonomy/plex-prometei-review/check.py
"""
from pathlib import Path
import struct, json, subprocess, tempfile, argparse

def check(out, cleave):
    root = Path(__file__).resolve().parents[3]
    cases = []
    loop = 'micro-behaviors/communications/http/url/host::loopback-http-url-reference'
    for (name, url, want) in [('ip', 'http://127.0.0.1:32400/status', True), ('localhost', 'https://localhost/api', True), ('prefix', 'http://127.0.0.1.collector.invalid/leak', False), ('localhost-prefix', 'http://localhost.collector.invalid/api', False)]:
        p = out / (name + '.py')
        p.write_text('URL = ' + repr(url) + '\n')
        cases.append((p, [loop] if want else [], [] if want else [loop]))

    def image(data):
        """Construct an inert PE with RET entry and read-only test data."""
        b = bytearray(132096)
        b[:2] = b'MZ'
        struct.pack_into('<I', b, 60, 128)
        b[128:132] = b'PE\x00\x00'
        struct.pack_into('<HHIIIHH', b, 132, 332, 2, 0, 0, 0, 224, 258)
        opt = 152
        struct.pack_into('<H', b, opt, 267)
        for (off, val) in {16: 4096, 20: 4096, 24: 8192, 28: 4194304, 32: 4096, 36: 512, 56: 143360, 60: 512, 92: 16}.items():
            struct.pack_into('<I', b, opt + off, val)
        struct.pack_into('<H', b, opt + 68, 3)
        for (i, (n, vs, rva, sz, raw, flags)) in enumerate([(b'.text', 512, 4096, 512, 512, 1610612768), (b'.rdata', 131072, 8192, 131072, 1024, 1073741888)]):
            struct.pack_into('<8sIIIIIIHHI', b, opt + 224 + 40 * i, n, vs, rva, sz, raw, 0, 0, 0, 0, flags)
        b[512] = 195
        b[1024:1024 + len(data)] = data
        return b
    schema = b'?&i=%s&r=%s&answ=%s&enckey=%s\x00'
    cmds = b'fgetnormal\x00' + b'x' * 40 + b'\x00fgetcrypt\x00'
    onion = b'http://abcdefghijklmnop.onion/renamed.cgi\x00'
    run = b'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Foo\x00'
    tor = 'well-known/malware/botnet/prometei::windows-prometei-tor-c2'
    rk = 'well-known/malware/botnet/prometei::windows-prometei-run-key'
    for (name, data, yes, no) in [('renamed-endpoint', schema + cmds + onion + run, [tor, rk], []), ('endpoint-only', b'http://abcdefghijklmnop.onion/cgi-bin/prometei.cgi\x00' + run, [], [tor, rk]), ('no-command-table', schema + onion + run, [], [tor, rk]), ('schema-only', schema + cmds, [], [tor, rk])]:
        p = out / (name + '.exe')
        p.write_bytes(image(data))
        cases.append((p, yes, no))
    xor = 'micro-behaviors/data/encoding::x86-countdown-rolling-xor-loop'
    code = bytes.fromhex('8a da 02 d9 30 18 85 c9 74 10 40 8d 98 12 34 56 78 49 03 d7 3b de 7c e8')
    for (name, payload, want) in [('rolling-xor', code, True), ('rolling-add', code.replace(b'0\x18', b'\x00\x18'), False)]:
        p = out / (name + '.exe')
        p.write_bytes(image(payload))
        cases.append((p, [xor] if want else [], [] if want else [xor]))
    cmd = [cleave, '--traits-dir', str(root), '--json'] + [str(p) for (p, _, _) in cases]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode:
        raise SystemExit(p.stderr[-5000:])
    reports = [json.loads(s) for s in p.stdout.splitlines() if s.strip()]
    bypath = {}
    for report in reports:
        for f in report.get('files', [report]):
            bypath[f.get('path', '')] = f
    for (path, yes, no) in cases:
        f = bypath.get(str(path))
        if f is None:
            raise SystemExit('missing ' + str(path) + ' keys ' + str(list(bypath)))
        traits = {t['id'] for t in f.get('traits', f.get('findings', []))}
        for t in yes:
            assert t in traits, ('missing', path.name, t)
        for t in no:
            assert t not in traits, ('unexpected', path.name, t)
        print('PASS', path.name)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='.controls-', dir=Path(__file__).parent) as directory:
        check(Path(directory).resolve(), args.cleave)
