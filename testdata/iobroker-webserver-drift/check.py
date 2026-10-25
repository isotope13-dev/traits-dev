#!/usr/bin/env python3
"""Check relocated observations, retained attacks, and nearby benign code."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--baseline', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
cases = args.scratch / 'runtime-cases'
cases.mkdir(parents=True, exist_ok=True)
for source in Path(__file__).parent.iterdir():
    if source.suffix in ('.js', '.py') and source.name != 'check.py':
        shutil.copyfile(source, cases / source.name)
# Existing fixtures outside this batch, also scanned in their original paths.
external = [root / 'testdata/benign/tls-context-only.js',
            root / 'testdata/taxonomy/pi-gated-cookie-reader/src/ungated-cookie-hijack/package/steal.js']

def scan(traits, tag):
    output = args.scratch / (tag + '.json')
    subprocess.run(['cleave', '--traits-dir', str(traits), '--format', 'json',
                    'analyze', *map(str, sorted(cases.iterdir())),
                    *map(str, external), '-o', str(output)], check=True)
    pending = output.read_text()
    decoder = json.JSONDecoder()
    files = {}
    while pending.strip():
        obj, end = decoder.raw_decode(pending.lstrip())
        pending = pending.lstrip()[end:]
        for item in obj.get('files', []):
            files[Path(item['path']).name] = {t['id']: t['crit'] for t in item.get('traits', [])}
    return files

current = scan(root, 'focused-after')
cookie = 'micro-behaviors/communications/http/cookie-store::cookie-search-near-auth-token-name'
replay = 'objectives/credential-access/browser/session-hijack::browser-cookie-replay-auth-token-harvest'
session = 'objectives/credential-access/browser/session-hijack::browser-cookie-store-session-replay'
context = 'micro-behaviors/communications/tls/initialize::node-tls-create-secure-context'
sni = 'micro-behaviors/communications/tls/initialize::javascript-sni-callback-option'
forward = 'micro-behaviors/communications/proxy/mitm::javascript-mitm-https-forwarding'
expiry = 'micro-behaviors/communications/http/token-auth::zero-token-expiry-field'
admin = 'micro-behaviors/communications/http/services/artifactory::nonexpiring-global-admin-token-request'
exploit = 'objectives/execution/exploit/access-control::artifactory-empty-key-admin-token-chain'
random = 'micro-behaviors/os/random/crypto::node-unbound-random-bytes-call'
checks = [
 ('cookie-replay.js', {cookie, replay, session}, set()),
 ('cookie-lookup.js', {cookie}, {replay, session}),
 ('cookie-no-token.js', set(), {cookie, replay, session}),
 ('tls-forward.js', {context, sni, forward}, set()),
 ('tls-server.js', {context, sni}, {forward}),
 ('tls-context-only.js', {context}, {forward, sni}),
 ('expiry-positive.py', {expiry, admin}, {exploit}),
 ('artifactory-chain.py', {expiry, admin, exploit}, set()),
 ('expiry-controls.js', set(), {expiry, admin, exploit}),
 ('random-call.js', {random}, set()),
 ('random-no-call.js', set(), {random}),
]
for name, required, forbidden in checks:
    got = current[name]
    assert required <= got.keys(), (name, 'missing', required - got.keys())
    assert not forbidden & got.keys(), (name, 'unexpected', forbidden & got.keys())
assert current['cookie-replay.js'][replay] == 5
assert current['artifactory-chain.py'][exploit] == 5
if args.baseline:
    previous = scan(args.baseline, 'focused-before')
    for name, ids in [('cookie-replay.js', {replay, session}),
                      ('tls-forward.js', {forward}),
                      ('artifactory-chain.py', {admin, exploit})]:
        for trait in ids:
            assert trait in previous[name] and current[name][trait] == previous[name][trait], (name, trait)
    # The pre-existing browser-store theft fixture retains all attack findings.
    for trait, crit in previous['steal.js'].items():
        if trait.startswith('objectives/'):
            assert current['steal.js'].get(trait) == crit, trait
print('11 focused cases and existing browser-store attack coverage passed')
