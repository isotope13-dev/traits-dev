#!/usr/bin/env python3
"""Check behavior roles against byte-preserving specimen mutations.

Usage: python3 check.py <dropped_payload.exe> <scratch-directory>
The specimens are only statically scanned; no target code is executed.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
sample = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
rules = {
    'session': 'objectives/exfiltration/stealer/token::native-telegram-session-archive-upload',
    'ransom': 'objectives/impact/ransom/encrypt/bulk-encryption::native-cryptoapi-file-io-ransom-demand',
    'miner': 'objectives/impact/cryptojacking/miner/pool::concealed-randomx-miner-logon-exclusions',
    'control': 'objectives/command-and-control/remote-command/task-schema::socket-ransom-surveillance-control-profile',
}
cases = {
    'original': ([], set()),
    'no-session-source': ([(b'Telegram Desktop\\tdata', b'Telegram Desktop\\cache')], {'session'}),
    'no-encrypt-api': ([(b'CryptEncrypt', b'CryptXncrypt')], {'ransom'}),
    'visible-launcher': ([(b'WindowStyle Hidden', b'WindowStyle Normal')], {'miner'}),
    # Two starts must not substitute for distinct start AND stop operations.
    'no-keylog-stop': ([(b'stop_keylogger\x00dos_getgateway',
                          b'start_keylogger\x00os_getgateway')], {'control'}),
    'no-ransom-demand': ([(b'Pay the ransom', b'Use this guide')], {'ransom', 'control'}),
}
original = sample.read_bytes()
paths = []
for name, (edits, absent) in cases.items():
    data = original
    for old, new in edits:
        assert len(old) == len(new) and old in data, (name, old)
        data = data.replace(old, new)
    path = scratch / (name + '.exe')
    path.write_bytes(data)
    paths.append(str(path))
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', *paths], text=True, capture_output=True, check=True,
)
(scratch / 'reports.jsonl').write_text(result.stdout)
(scratch / 'scan.log').write_text(result.stderr)
# Multi-target output is a stream of complete JSON reports.
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
reports = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
by_name = {}
for report in reports:
    for file in report['files']:
        if '!!' not in file['path']:
            by_name[Path(file['path']).stem] = {
                trait['id'] for trait in file.get('traits', [])
            }
for name, (_, absent) in cases.items():
    seen = by_name[name]
    for label, rule in rules.items():
        assert (rule in seen) == (label not in absent), (name, label)
    assert 'objectives/anti-analysis/debugger-detect/tls::multi-tls-callbacks-with-analysis-catalog' not in seen
    print(name + ': passed')

source_dir = Path(__file__).parent
source_names = ['git-exec.js', 'git-direct.js', 'git-instructions.js', 'status-loop.js']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', *[str(source_dir / name) for name in source_names]],
    text=True, capture_output=True, check=True,
)
remaining = result.stdout.lstrip()
source_reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report['files']:
        source_reports[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
git_prefix = 'micro-behaviors/process/create/shell/git::'
assert git_prefix + 'jake-git-command-array' in source_reports['git-exec.js']
assert git_prefix + 'git-shell-command-call' in source_reports['git-direct.js']
assert not any(t.startswith(git_prefix) for t in source_reports['git-instructions.js'])
assert 'micro-behaviors/data/control-flow/status::for-header-status-word' in source_reports['status-loop.js']
assert not any('http/device-code' in t for t in source_reports['status-loop.js'])
print('four source controls: passed')
