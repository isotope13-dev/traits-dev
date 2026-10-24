#!/usr/bin/env python3
"""Exercise static source relationships without compiling or running them."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORT = 'objectives/exfiltration/stealer/multi-source::rust-cookie-config-buffer-tcp-export'
HOSTILE = 'objectives/exfiltration/stealer/multi-source::rust-vm-gated-cookie-config-export'
LOOKUP = 'micro-behaviors/dylib/lookup::rust-helper-result-api-name'
START = 'micro-behaviors/process/inject/remote-thread::allocated-memory-remote-thread-start'
parser = argparse.ArgumentParser()
parser.add_argument('--fixture-parent', type=Path)
parser.add_argument('--sample', type=Path)
args = parser.parse_args()
cases = []
def add(name, source, present=(), absent=()):
    cases.append((name, source, set(present), set(absent)))

transfer = (HERE / 'transfer.rs').read_text()
lookup = (HERE / 'lookup.rs').read_text()
allocated = (HERE / 'allocated.rs').read_text()
add('transfer.rs', transfer, [EXPORT], [HOSTILE])
add('renamed.rs', re.sub(r'\b(combined|relative|path|content|packet|channel|transform)\b',
    lambda m: 'new_' + m[0], transfer), [EXPORT], [HOSTILE])
add('reordered.rs', transfer.replace('"mRemoteNG\\\\confCons.xml", "Mozilla\\\\Firefox\\\\Profiles\\\\cookies.sqlite"',
    '"Mozilla\\\\Firefox\\\\Profiles\\\\cookies.sqlite", "mRemoteNG\\\\confCons.xml"'), [EXPORT])
for name, old, new in [
    ('different-join', '.join(relative)', '.join(other)'),
    ('different-path', 'fs::read(&path)', 'fs::read(&other)'),
    ('different-read-result', 'extend_from_slice(&content)', 'extend_from_slice(&other)'),
    ('different-accumulator', 'transform(&combined,', 'transform(&other,'),
    ('different-packet', 'write_all(&packet)', 'write_all(&other)'),
    ('different-stream', 'channel.write_all', 'other.write_all'),
    ('local-backup', 'channel.write_all', 'fs::write'),
    ('ordinary-file', 'cookies.sqlite', 'preferences.json'),
    ('ordinary-config', 'confCons.xml', 'preferences.xml'),
    ('path-shadow', 'if let Ok(content)', 'let path = other; if let Ok(content)'),
    ('packet-shadow', 'let _ = channel.write_all', 'let packet = other; let _ = channel.write_all'),
    ('comment-target', '"mRemoteNG\\\\confCons.xml"', '"settings.json" /* confCons.xml */'),
]:
    assert old in transfer, name
    add(name + '.rs', transfer.replace(old, new), absent=[EXPORT, HOSTILE])
add('comment.rs', '\n'.join('// ' + line for line in transfer.splitlines()), absent=[EXPORT, HOSTILE])
add('lookup.rs', lookup, [LOOKUP])
add('lookup-other.rs', lookup.replace('result.as_ptr()', 'other.as_ptr()'), absent=[LOOKUP])
add('allocated.rs', allocated, [START])
add('allocated-other.rs', allocated.replace('0, address,', '0, other,'), absent=[START])
add('allocated-literal.rs', allocated.replace('0, address,', '0, 4096,'), absent=[START])
if args.sample:
    source = args.sample.read_text()
    add('agent.rs', source, [EXPORT, HOSTILE, LOOKUP, START])
    add('agent-without-vm-gate.rs', source.replace('process::exit(0);', 'return false;'), [EXPORT], [HOSTILE])
    add('agent-unrelated-send.rs', source.replace('stream.write_all(&packet)', 'stream.write_all(&other)'), [LOOKUP, START], [EXPORT, HOSTILE])
with tempfile.TemporaryDirectory(prefix='rust-export-', dir=args.fixture_parent) as directory:
    for name, source, _, _ in cases:
        (Path(directory) / name).write_text(source)
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', directory], capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    remaining, observed = result.stdout, {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report['files']:
            observed[Path(file['path']).name] = {t['id']: t for t in file.get('traits', [])}
    checks = 0
    for name, _, present, absent in cases:
        for trait in present:
            assert trait in observed[name], (name, 'missing', trait)
            if trait == HOSTILE:
                assert observed[name][trait]['crit'] == 5
            checks += 1
        for trait in absent:
            assert trait not in observed[name], (name, 'unexpected', trait)
            checks += 1
    print(f'{checks} assertions passed across {len(cases)} source controls')
