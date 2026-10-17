#!/usr/bin/env python3
"""Verify command observations and distinguish encoded search data from sinks."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='shell-context-', dir=root) as temp:
    for source in fixtures.glob('*.sh'):
        shutil.copyfile(source, Path(temp) / source.name)
    result = subprocess.run(
        ['cleave', '--traits-dir', str(root), '--format', 'json', temp],
        capture_output=True, text=True, check=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout
    observations = {}
    while remaining.strip():
        report, consumed = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[consumed:]
        for file in report['files']:
            if '##' not in file['path']:
                observations[Path(file['path']).name] = {
                    trait['id'] for trait in file['traits']
                }

positive = observations['operations.sh']
negative = observations['references.sh']
for trait in [
    'metadata/build/package-builder::fpm-reference',
    'micro-behaviors/communications/icmp/trace::tracepath',
    'micro-behaviors/data/parse/regex::grep-matching-substrings',
    'micro-behaviors/os/package-manager/install::apt-get-install-cmd',
    'micro-behaviors/os/package-manager/install::yum-install-cmd',
    'micro-behaviors/fs/attributes/chattr::authorized-keys-set-immutable',
    'micro-behaviors/process/create/local-exec::tmp-path-execution',
    'micro-behaviors/process/create/shell/spawn::shell-execution-shm',
    'objectives/evasion/masquerade/process/path::system-service-masquerade',
]:
    assert trait in positive, ('missing operation', trait)
    assert trait not in negative, ('reference treated as operation', trait)
for trait in [
    'objectives/persistence/login/ssh/backdoor::ssh-key-immutable-persistence',
    'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-malicious-shell',
    'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-pipe-to-shell',
    'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-curl-wget',
]:
    assert trait not in negative, ('inert data treated as execution', trait)
for trait in [
    'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-pipe-to-shell',
    'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-curl-wget',
]:
    assert trait in observations['encoded-sink.sh'], ('lost execution sink', trait)
for trait in [
    'objectives/impact/degrade/services::cloud-agent-removal-with-miner-killing',
    'objectives/persistence/system/cron/schedule::recurring-fetch-shell-with-agent-removal',
]:
    assert trait in observations['cron-agent-removal.sh'], ('lost hostile behavior', trait)
assert 'objectives/persistence/login/ssh/backdoor::ssh-key-immutable-persistence' in observations['key-install.sh'], 'lost key installation and lock'
print('PASS: command, encoding, key-attribute, and cron behavior boundaries')
