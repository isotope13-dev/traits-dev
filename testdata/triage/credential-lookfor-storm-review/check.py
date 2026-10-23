"""Check saved Cleave control scans (baseline and corrected rules).

Usage: python3 check.py <review scratch directory>
The review.json records how real native specimens and source controls were made.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
def reports(name):
    remaining = (root / name).read_text()
    decoder = json.JSONDecoder()
    result = {}
    while remaining.strip():
        remaining = remaining.lstrip()
        obj, consumed = decoder.raw_decode(remaining)
        remaining = remaining[consumed:]
        for entry in obj['files']:
            result[Path(entry['path']).name] = {t['id']: t['crit'] for t in entry.get('traits', [])}
    return result

before = reports('controls.before.json')
after = reports('controls.after.json')
checks = []
def expect(name, trait, present=True):
    actual = trait in after[name]
    assert actual == present, (name, trait, present, actual)
    checks.append([name, trait, present])

collection = 'objectives/collection/file-copy/sensitive::phished-secret-store-copies'
export = 'objectives/exfiltration/stealer/multi-source::phished-secret-staging-archive-upload'
wallet = 'objectives/evasion/masquerade/process/app-substitute::'
for suffix in ['applescript', 'js']:
    expect('renamed-staging.' + suffix, collection)
    expect('renamed-staging.' + suffix, export)
    expect('local-secret-staging.' + suffix, collection)
    expect('local-secret-staging.' + suffix, export, False)
    for name in ['backup-upload', 'ordinary-updater', 'keychain-only']:
        expect(name + '.' + suffix, collection, False)
        expect(name + '.' + suffix, export, False)
expect('wallet-no-phish.js', wallet + 'wallet-resource-copy-adhoc')
expect('wallet-no-phish.js', wallet + 'wallet-resource-phish-replacement', False)
body = 'micro-behaviors/communications/http/upload::curl-data-binary-file-body'
for name in ['put', 'post', 'quote']:
    expect('body-' + name + '.sh', body)
expect('body-put.sh', 'micro-behaviors/fs/path/archive::curl-archive-update-filename')
expect('body-put.sh', 'micro-behaviors/communications/http/download/curl::source-curl-archive-output', False)
for name in ['raw', 'stdin']:
    expect('body-' + name + '.sh', body, False)
imports = 'objectives/anti-static/obfuscation/imports/concealment::fragment-loader-export-backscan'
execute = 'objectives/anti-static/obfuscation/payload/fragmentation::fragment-loader-executable-buffer'
corpus = 'objectives/anti-static/obfuscation/string/junking::fragment-loader-hash-path-corpus'
for trait in [imports, execute, corpus]:
    expect('loader-renamed.exe', trait)
    expect('loader-no-fragment-reassembly.exe', trait, False)
expect('loader-no-ballast.exe', imports)
expect('loader-no-ballast.exe', execute)
expect('loader-no-ballast.exe', corpus, False)
expect('loader-no-execute-protection.exe', imports)
expect('loader-no-execute-protection.exe', corpus)
expect('loader-no-execute-protection.exe', execute, False)
tls = 'micro-behaviors/communications/tls/verify/disable::x86-wininet-ignore-certificate-name-date'
expect('tls-positive.exe', tls)
expect('tls-verified.exe', tls, False)
expect('tls-unrelated-call.exe', tls, False)

moves = {
    'objectives/credential-access/files/secret-sweep::validated-password-with-secret-store-copies': collection,
    'objectives/supply-chain/trojanized/app/wallet::wallet-resource-copy-adhoc': wallet + 'wallet-resource-copy-adhoc',
    'objectives/supply-chain/trojanized/app/wallet::wallet-resource-phish-replacement': wallet + 'wallet-resource-phish-replacement',
}
unsupported = {
    'objectives/anti-analysis/sandbox-detect/environment/path::sandbox-hash-path-fragment-loader',
    'objectives/command-and-control/dropper/staging/temp::concealed-import-user-dir-exe-dropper',
}
# Every previously emitted hostile/suspicious observation survives, except the
# two documented unsupported claims; placement moves retain criticality.
for name, traits in before.items():
    for trait, criticality in traits.items():
        if criticality >= 4 and trait not in unsupported:
            target = moves.get(trait, trait)
            assert after[name].get(target, 0) >= criticality, (name, trait, 'lost')
print(f'PASS: {len(checks)} assertions across {len(after)} real/source controls; retained H/S coverage')
(root / 'focused-checks.json').write_text(json.dumps({'checks': checks, 'controls': len(after), 'retained_coverage': True}, indent=2))
