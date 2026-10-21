#!/usr/bin/env python3
"""Check source/send separation and retained attack coverage without execution."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OOB = 'micro-behaviors/communications/url/host/oob::'
EXPORT = 'objectives/exfiltration/stealer/system-info/identity::npm-postinstall-oast-hostname-get'
GET = 'micro-behaviors/communications/http/get::npm-postinstall-node-http-get'
REQUIRE = 'micro-behaviors/os/module/require::postinstall-bare-module-require'
WALLET = 'objectives/exfiltration/stealer/wallet::wallet-seed-field-concealed-post-pattern'
DECEPTION = 'objectives/evasion/masquerade/extension/deception::false-no-data-claim-seed-phrase-upload'
CASES = {}
for name in ['endpoint-echo', 'identity-without-send', 'unrelated-get', 'hostname-benign-get']:
    required = [OOB + 'manifest-oast-fun-reference']
    if name != 'endpoint-echo':
        required.append(OOB + 'postinstall-identity-query-oob-reference')
    CASES[HERE / name / 'package.json'] = (required, [EXPORT])
CASES[HERE / 'hostname-wrong-oast-suffix/package.json'] = ([GET], [EXPORT])
CASES[HERE / 'hostname-oast-get/package.json'] = ([EXPORT, GET, REQUIRE], [])
for name in ['bare-module', 'builtin-module']:
    CASES[HERE / name / 'package.json'] = ([REQUIRE], [EXPORT])
CASES[HERE / 'relative-module/package.json'] = ([], [REQUIRE, EXPORT])
for name in ['seed-fields-get-only.zip', 'seed-fields-no-collection.zip']:
    CASES[HERE / name] = ([], [WALLET, DECEPTION])
CASES[ROOT / 'testdata/triage/registry-extension-review/concealed-wallet.zip'] = ([WALLET, DECEPTION], [])
CASES[ROOT / 'testdata/triage/registry-extension-review/ordinary-wallet.zip'] = ([], [WALLET, DECEPTION])
CASES[ROOT / 'testdata/triage/pinned-release-controls/oast-postinstall.tgz'] = ([
    'objectives/supply-chain/recon-exfil/npm-install-targeting::js-sysinfo-oast-https-post-exfil'], [])
CASES[ROOT / 'testdata/hostile/lifecycle-jwt-oast.tgz'] = ([
    'objectives/supply-chain/recon-exfil/oast/secret::lifecycle-jwt-sweep-oast-exfil'], [])
CASES[ROOT / 'testdata/npm-install-hook-oast-exfil/inline-dropper.tgz'] = ([
    'objectives/supply-chain/recon-exfil/inline::postinstall-etc-oastify-b64-exfil'], [])
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
    '--format', 'json', *map(str, CASES)], capture_output=True, text=True, cwd=ROOT)
if result.returncode:
    raise SystemExit(result.stderr)
reports = {}
s = result.stdout
while s.strip():
    report, end = json.JSONDecoder().raw_decode(s.lstrip())
    s = s.lstrip()[end:]
    reports.update({f['path']: f for f in report['files']})
for path, (required, forbidden) in CASES.items():
    ids = {t['id'] for t in reports[str(path)].get('traits', [])}
    assert set(required) <= ids, (path, 'missing', set(required) - ids)
    assert not set(forbidden) & ids, (path, 'unexpected', set(forbidden) & ids)
print(f'{len(CASES)} source/send and retained-attack controls passed')
