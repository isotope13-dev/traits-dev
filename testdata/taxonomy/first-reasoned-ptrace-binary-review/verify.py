"""Inert controls for policy vocabulary, overlay identity and process signals."""
import base64
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
UAC = 'micro-behaviors/os/security/policy::base64-uac-zero-write-script'
XW = 'well-known/malware/rat/xworm::xworm-embedded-client'
SIGNAL = 'micro-behaviors/process/control/signal::js-kill-with-signal-flag'
TERM = 'micro-behaviors/process/terminate/command::js-kill-with-termination-signal'
WRITE = 'micro-behaviors/process/attach/debugger::node-procfs-ptrace-write-profile'
OLD = 'objectives/evasion/process/injection/ptrace::aix-node-procfs-ptrace-injection'

def pe(blob=b'', overlay=b'', section='.rdata', code=b'\xc3'):
    h = bytearray(512)
    h[:2] = b'MZ'
    struct.pack_into('<I', h, 60, 128)
    h[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', h, 132, 0x14c, 2, 0, 0, 0, 224, 0x102)
    o = 152
    struct.pack_into('<H', h, o, 0x10b)
    struct.pack_into('<I', h, o + 16, 4096)
    struct.pack_into('<I', h, o + 28, 0x400000)
    struct.pack_into('<II', h, o + 32, 4096, 512)
    struct.pack_into('<II', h, o + 56, 16384, 512)
    struct.pack_into('<H', h, o + 68, 3)
    struct.pack_into('<I', h, o + 92, 16)
    for i, name, content, offset, size, flags in [
        (0, '.text', code, 512, 512, 0x60000020),
        (1, section, blob, 1024, 4096, 0x40000040),
    ]:
        assert len(content) <= size
        struct.pack_into('<8sIIIIIIHHI', h, 376 + i * 40,
                         name.encode(), max(1, len(content)), 4096 * (i + 1),
                         size, offset, 0, 0, 0, 0, flags)
    return bytes(h) + code.ljust(512, b'\0') + blob.ljust(4096, b'\0') + overlay

def scan(path):
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
        str(ROOT), '--format', 'json', str(path)], text=True,
        capture_output=True, check=True)
    decoder = json.JSONDecoder()
    rest = result.stdout.strip()
    reports = {}
    while rest:
        doc, end = decoder.raw_decode(rest)
        rest = rest[end:].lstrip()
        for f in doc.get('files', [doc]):
            reports[Path(f['path']).name] = f
    return reports

def main():
    dest = Path(sys.argv[1]); dest.mkdir(parents=True, exist_ok=True)
    script = (b'$p="HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"\n'
              b'$n="EnableLUA"\nSet-ItemProperty -Path $p -Name $n -Value 0\n')
    payload = (bytes.fromhex('4d5a90000300000004000000ffff0000') + b'\0BSJB\0\0' +
               b''.join(x.encode('utf-16le') + b'\0\0' for x in
                        ['Urlhide', 'PCShutdown', 'RunShell', 'OfflineGet']))
    cases = {}
    for pad in range(3):
        cases[f'uac-{pad}.exe'] = (pe(base64.b64encode(b' ' * pad + script)), {UAC}, set())
    cases.update({
        'uac-enabled.exe': (pe(base64.b64encode(script.replace(b'-Value 0', b'-Value 1'))), set(), {UAC}),
        'other-policy.exe': (pe(base64.b64encode(script.replace(b'EnableLUA', b'OtherKey'))), set(), {UAC}),
        'unrelated-zero.exe': (pe(base64.b64encode(script.replace(b'Set-ItemProperty', b'x' * 600 + b'Set-ItemProperty'))), set(), {UAC}),
        'data-policy.exe': (pe(base64.b64encode(script), section='.data'), set(), {UAC}),
        'xworm-overlay.exe': (pe(overlay=payload), {XW}, set()),
        'xworm-rdata.exe': (pe(blob=payload), {XW}, set()),
        'overlay-commands-only.exe': (pe(overlay=payload[16:]), set(), {XW}),
        'overlay-subset.exe': (pe(overlay=payload.replace('RunShell'.encode('utf-16le'), b'X' * 16)), set(), {XW}),
        'terminate.js': (b"const {execSync} = require('child_process'); execSync('kill -9 1234');", {SIGNAL, TERM}, set()),
        'member-terminate.js': (b"const cp=require('child_process'); cp.execSync('kill -TERM 1234');", {SIGNAL, TERM}, set()),
        'stop.js': (b"const {execSync} = require('child_process'); execSync('kill -STOP 1234');", {SIGNAL}, {TERM}),
        'continue.js': (b"const {execSync} = require('child_process'); execSync('kill -CONT 1234');", {SIGNAL}, {TERM}),
        'signal-doc.js': (b"console.log('kill -9 1234');", set(), {SIGNAL, TERM}),
        'ptrace-patch.js': (b"const fs=require('fs'); const {ptrace,PT_ATTACH,PT_WRITE_I}=require('aix-ptrace'); const pid=process.argv[2]; fs.openSync(`/proc/${pid}/as`,'r+'); ptrace(pid,PT_ATTACH,0,0); ptrace(pid,PT_WRITE_I,0,1);", {WRITE}, {OLD}),
        'ptrace-path-only.js': (b"const path=`/proc/${pid}/as`;", set(), {WRITE, OLD}),
    })
    for name, (content, _, _) in cases.items(): (dest / name).write_bytes(content)
    reports = scan(dest)
    for name, (_, yes, no) in cases.items():
        traits = {t['id'] for t in reports[name]['traits']}
        assert yes <= traits, (name, 'missing', yes - traits)
        assert not no & traits, (name, 'unexpected', no & traits)
    # Verify the wallet-path consumer as well as the standalone signal facts.
    real = ROOT / 'testdata/taxonomy/first-reasoned-ptrace-binary-review/wallet-terminate.js'
    r = scan(real)[real.name]
    ts = {t['id'] for t in r['traits']}
    assert TERM in ts, ('wallet fixture lost termination', ts)
    assert 'micro-behaviors/process/terminate/command::application-path-force-kill' in ts
    # Existing fixtures retain Windows wallet interference and Linux ptrace.
    for rel, expected in [
        ('testdata/taxonomy/wallet-ui/interference.js',
         'objectives/impact/degrade/process::hidden-window-wallet-process-interference'),
        ('testdata/taxonomy/ptrace-name-table-retirement/positive/call-plus-diagnostics.c',
         'micro-behaviors/process/inject/memory::ptrace-poke-source-call'),
    ]:
        fixture = ROOT / rel
        traits = {t['id'] for t in scan(fixture)[fixture.name]['traits']}
        assert expected in traits, (rel, 'lost existing coverage', expected)
    print(f'{len(cases)} controls, wallet consumer and 2 existing fixtures passed')

if __name__ == '__main__': main()
