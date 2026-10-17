#!/usr/bin/env python3
"""Check original artifacts and transport/scope controls without executing code."""
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PROFILE = 'micro-behaviors/os/sysinfo/profile::shell-host-queries-discord-post'
HOOK = 'micro-behaviors/os/sysinfo/profile::npm-install-shell-survey-webhook'
RETIRED = {
    'objectives/exfiltration/stealer/multi-source::install-hook-recon-discord-webhook',
    'objectives/supply-chain/install-hook/scripts/host-recon::install-hook-postinstall-shell-host-recon',
    'objectives/supply-chain/impersonation/npm-clone::bn-js-clone-next-runtimejs-payload',
    'objectives/supply-chain/trojanized/hidden-dependency::trojanized-library-next-runtimejs-loader',
}

def read_members(path):
    with tarfile.open(path) as archive:
        return {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}

def write_archive(path, members):
    with tarfile.open(path, 'w:gz') as archive:
        for name, content in members.items():
            member = tarfile.TarInfo(name)
            member.size = len(content)
            archive.addfile(member, io.BytesIO(content))

with tempfile.TemporaryDirectory(prefix='.telemetry-review-', dir=ROOT) as staging:
    staging = Path(staging)
    cases = []
    for name, expected in [('discord-postinstall.tgz', 1),
                           ('discord-notify-postinstall.tgz', 0),
                           ('bnjs-next-runtimejs.tgz', 0)]:
        target = staging / name
        shutil.copyfile(ROOT / 'testdata/benign' / name, target)
        cases.append((target, expected, name == 'discord-postinstall.tgz'))

    members = read_members(ROOT / 'testdata/benign/discord-postinstall.tgz')
    script_key = 'package/scripts/postinstall.sh'
    script = members[script_key]
    queries, post = script.rsplit(b'curl ', 1)
    controls = {
        'no-send.tgz': {**members, script_key: queries},
        'endpoint-only.tgz': {**members, script_key: queries + b'printf "%s\\n" "https://discord.com/api/webhooks/12345/token"\n'},
        'split-members.tgz': {**members, script_key: queries, 'package/scripts/notify.sh': b'#!/bin/sh\ncurl ' + post},
    }
    for name, content in controls.items():
        target = staging / name
        write_archive(target, content)
        cases.append((target, 0, False))

    bn = read_members(ROOT / 'testdata/benign/bnjs-next-runtimejs.tgz')
    renamed = {name: content.replace(b'next-runtimejs', b'ordinary-runtime') for name, content in bn.items()}
    target = staging / 'renamed-dependency.tgz'
    write_archive(target, renamed)
    cases.append((target, 0, False))

    command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json']
    result = subprocess.run(command + [str(c[0]) for c in cases], text=True, capture_output=True, check=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        report, consumed = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[consumed:].lstrip()
    for target, suspicious, profile in cases:
        report = next(f for f in files if f['path'] == str(target))
        traits = {t['id']: t for t in report.get('traits', [])}
        assert not RETIRED.intersection(traits), (target.name, 'retired conviction')
        assert not [t for t in traits.values() if t['crit'] == 5], (target.name, 'hostile')
        observed = [t['id'] for t in traits.values() if t['crit'] == 4]
        assert len(observed) == suspicious, (target.name, observed)
        assert (PROFILE in traits) == profile, (target.name, 'profile')
        assert (HOOK in traits) == profile, (target.name, 'hook')
        print(target.name, 'PASS', suspicious, 'suspicious, 0 hostile')
