#!/usr/bin/env python3
"""Check configuration observations without attributing compromise or transfer."""
import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
WRITE = 'micro-behaviors/fs/write/content::npm-postinstall-claude-settings-write-cooccurrence'
PREFIX = 'micro-behaviors/os/telemetry/logging/llm::'
CONTENT = PREFIX + 'npm-postinstall-content-export-cooccurrence'
BEARER = PREFIX + 'npm-postinstall-hardcoded-content-export-cooccurrence'
GLOBAL = PREFIX + 'global-agent-content-telemetry-write'
RETIRED = {
    'objectives/supply-chain/install-hook/agent::npm-postinstall-writes-claude-global-settings',
    'objectives/supply-chain/install-hook/agent::npm-postinstall-plants-global-prompt-telemetry',
    'objectives/supply-chain/install-hook/persistence::npm-postinstall-persists-agent-content-collection',
}
parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
with tarfile.open(ROOT / 'testdata/suspicious/postinstall-prompt-telemetry.tgz') as archive:
    members = {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}
script_key = 'package/scripts/setup.js'
source = members[script_key]
manifest_key = 'package/package.json'
no_hook = json.loads(members[manifest_key])
no_hook.pop('scripts')
local = source.replace(b"path.join(os.homedir(), '.claude')", b"path.join(process.cwd(), '.claude')")
no_bearer = b'\n'.join(line for line in source.splitlines() if b'OTEL_EXPORTER_OTLP_HEADERS' not in line)
no_write = b'\n'.join(line for line in source.splitlines() if b'fs.writeFileSync' not in line)
renamed = {name: data.replace(b'agent-telemetry-helper', b'unrelated-tool').replace(
    b'otel-collector-7d2af1.example.net', b'collector.example.org') for name, data in members.items()}
# Deliberately split the global path/write and content configuration: the
# archive observations remain true, but the file-scoped warning must disappear.
settings_lines = b'\n'.join(line for line in source.splitlines() if b'OTEL_' in line)
split = {**members, script_key: b'\n'.join(line for line in source.splitlines() if b'OTEL_' not in line),
         'package/config.js': settings_lines}
cases = [
    ('global-content', members, {WRITE, CONTENT, BEARER, GLOBAL}, set(), 1),
    ('metrics', None, {WRITE}, {CONTENT, BEARER, GLOBAL}, 0),
    ('no-hook', {**members, manifest_key: json.dumps(no_hook).encode()}, {GLOBAL}, {WRITE, CONTENT, BEARER}, 1),
    ('project-local', {**members, script_key: local}, set(), {WRITE, CONTENT, BEARER, GLOBAL}, 0),
    ('no-write', {**members, script_key: no_write}, set(), {WRITE, CONTENT, BEARER, GLOBAL}, 0),
    ('no-bearer', {**members, script_key: no_bearer}, {WRITE, CONTENT, GLOBAL}, {BEARER}, 1),
    ('renamed', renamed, {WRITE, CONTENT, BEARER, GLOBAL}, set(), 1),
    ('split-members', split, {WRITE, CONTENT, BEARER}, {GLOBAL}, 0),
]
with tempfile.TemporaryDirectory(prefix='toga-version-drift-', dir=args.scratch) as staging:
    targets = []
    for name, content, *_ in cases:
        target = Path(staging) / (name + '.tgz')
        if content is None:
            target.write_bytes((ROOT / 'testdata/benign/otel-metrics-only-postinstall.tgz').read_bytes())
        else:
            with tarfile.open(target, 'w:gz') as archive:
                for member_name, data in content.items():
                    member = tarfile.TarInfo(member_name)
                    member.size = len(data)
                    archive.addfile(member, io.BytesIO(data))
        targets.append(target)
    command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json']
    result = subprocess.run(command + list(map(str, targets)), text=True, capture_output=True, check=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        report, consumed = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[consumed:].lstrip()
    for (name, _, required, forbidden, suspicious), target in zip(cases, targets):
        selected = [f for f in files if f['path'] == str(target) or f['path'].startswith(str(target) + '!!')]
        traits = {t['id']: t for f in selected for t in f.get('traits', [])}
        assert required <= traits.keys(), (name, 'missing', required - traits.keys())
        assert not (forbidden | RETIRED) & traits.keys(), (name, 'forbidden', (forbidden | RETIRED) & traits.keys())
        assert not [t for t in traits.values() if t['crit'] == 5], (name, 'hostile')
        observed = [t['id'] for t in traits.values() if t['crit'] == 4]
        assert len(observed) == suspicious, (name, observed)
        print(name, 'PASS;', suspicious, 'suspicious, 0 hostile')
