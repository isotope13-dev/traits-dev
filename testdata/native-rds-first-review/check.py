#!/usr/bin/env python3
"""Static regression controls; never execute the supplied PE or browser code.
Usage: check.py REMCOS SALAT HTML SCRATCH_DIRECTORY
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
remcos, salat, html, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
expected = ['72b9d4cb02bff5b716feba954b14d5d1723118dadf987677cd6ed0ba11c32e7d',
            '29e67b1723a5616c3f02ab2ef3bcf01cc538c80650cd0612a0bd1d0d54b047ef',
            '4946aff5d069639246a6afdf7923e9839099bc50e019e5da87784bfb17b2e79c']
for path, sha in zip([remcos, salat, html], expected):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha, path
SHELL = 'micro-behaviors/os/registry/manipulate::native-winlogon-shell-appended-path-writer'
PERSIST = 'well-known/malware/rat/remcos::remcos-native-winlogon-shell-writer'
UAC = 'objectives/evasion/security-bypass/policy/uac::native-network-keylogger-uac-disable-command'
GRAPH = 'micro-behaviors/communications/http/client/exchange::go-collector-http-call-chain'
UPLOAD = 'objectives/exfiltration/stealer/multi-source::go-browser-surveillance-collector-http-upload'
FRAGMENT = 'micro-behaviors/fs/file/read-write::js-concatenated-adodb-stream-progid'
OBF = 'objectives/anti-static/obfuscation/string/concat::rds-downloader-concatenated-stream-progid'
RDS = 'objectives/execution/activex/com::rds-http-response-save-and-launch'
THEFT = 'objectives/credential-access/browser/chromium::go-browser-login-query-with-keylogging'
KEYLOG = 'objectives/collection/keylog/hook::keyboard-hook-winsock-client'
CLEANUP = 'micro-behaviors/fs/delete/file/self::wide-wsh-script-self-delete-command'
CASES = {remcos: ({SHELL, PERSIST, UAC, CLEANUP}, set()), salat: ({GRAPH, UPLOAD, THEFT}, set()), html: ({RDS, OBF, FRAGMENT}, set())}

def case(name, data, yes, no):
    p = scratch / name
    p.write_bytes(data)
    CASES[p] = (set(yes), set(no))

# Keep the strings, registry APIs and concatenation code, but redirect the
# prefix operands away from both comma-terminated executable strings.
r = bytearray(remcos.read_bytes())
for off in [0x7eb3, 0x7f2b]:
    assert r[off] == 0x68
    r[off+1:off+5] = (0x415170).to_bytes(4, 'little')
case('unrelated-prefix.exe', r, [KEYLOG, UAC], [SHELL, PERSIST])
r = remcos.read_bytes()
needle = b'/t REG_DWORD /d 0 /f'
assert r.count(needle) == 1
case('uac-enable.exe', r.replace(needle, b'/t REG_DWORD /d 1 /f'), [SHELL, PERSIST, KEYLOG], [UAC])
r = remcos.read_bytes()
needle = 'Wscript.ScriptFullName'.encode('utf-16le')
assert r.count(needle) == 2
case('no-script-self-delete.exe', r.replace(needle, 'Wscript.ScriptOtherOne'.encode('utf-16le')), [SHELL, PERSIST, UAC], [CLEANUP])

# These mutations retain all names and theft code. They remove one actual
# CALL edge at a time, distinguishing a call chain from string co-occurrence.
for name, offset in [('collector-no-request.exe', 0x4e7ee0), ('helper-no-send.exe', 0x4d42e4)]:
    s = bytearray(salat.read_bytes())
    assert s[offset] == 0xe8
    s[offset:offset+5] = b'\x90' * 5
    case(name, s, [THEFT], [GRAPH, UPLOAD])

h = html.read_bytes()
case('renamed-endpoint.html', h.replace(b'enterinmind.com', b'example.invalid'), [RDS, OBF, FRAGMENT], [])
case('save-only.html', h.replace(b'.ShellExecute(fn)', b'.ignoreFile(fn)'), [FRAGMENT], [RDS, OBF])
case('ordinary-com-helper.html', b'<script>var stream = new ActiveXObject("adod"+"b.stream");</script>', [FRAGMENT], [RDS, OBF])
for name, yes, no in [('rds-save-launch.html', [RDS], [OBF]), ('rds-save-only.html', [], [RDS, OBF])]:
    CASES[ROOT / 'testdata/registry-source-62ad-3c7b-36c2' / name] = (set(yes), set(no))

cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl', *map(str, CASES)]
proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
(scratch / 'scans.jsonl').write_text(proc.stdout)
(scratch / 'scans.stderr').write_text(proc.stderr)
files = [f for line in proc.stdout.split('\n') if line for f in json.loads(line)['files']]
for path, (yes, no) in CASES.items():
    file = next(f for f in files if f['path'] == str(path))
    ids = {t['id'] for t in file.get('traits', [])}
    assert yes <= ids, (str(path), 'missing', yes - ids)
    assert not no & ids, (str(path), 'unexpected', no & ids)
    if path.name == 'ordinary-com-helper.html':
        assert not any(t['crit'] >= 4 for t in file.get('traits', [])), file
    print('PASS', path.name)
print('Passed', len(CASES), 'static cases')
