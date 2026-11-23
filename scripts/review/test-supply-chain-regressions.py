#!/usr/bin/env python3
"""Assert the individual traits behind representative supply-chain findings."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
PYTHON = 'python-startup-credential-collection'
BROWSER = 'browser-supply-chain'

PTH = 'objectives/persistence/system/python-startup::wheel-pth-with-credential-stealer'
CUSTOMIZE = 'objectives/persistence/system/python-startup::customize-hook-with-credential-stealer'
PROC = 'objectives/exfiltration/stealer/credential/environment/other-process::python-proc-secrets-encoded-upload'
ENV = 'objectives/exfiltration/stealer/credential/environment/current-process::python-env-sweep-concealed-upload'
CI = 'objectives/credential-access/api-harvest/ci-oidc::stealer-requests-ci-federation'
IDENTITY = 'objectives/credential-access/cloud/instance-role::stealer-requests-managed-identity'
ENCODED_COPY = 'objectives/anti-static/obfuscation/eval/browser::reversed-base64-clipboard-interceptor'
COPY = 'objectives/impact/crypto-manipulation/hijack-transfer/address::browser-copy-event-wallet-rewrite'
CARD = 'objectives/exfiltration/stealer/financial/payment-card::intercepted-card-beacon'
CARD_FETCH = 'objectives/exfiltration/stealer/financial/payment-card::live-card-input-value-fetch'
CARD_SOCKET = 'objectives/exfiltration/stealer/financial/payment-card::credit-card-websocket-stealer'
CARD_BEACON = 'objectives/exfiltration/stealer/financial/payment-card::live-card-input-value-beacon'
CARD_AND_COPY = 'objectives/exfiltration/stealer/financial/payment-card::browser-copy-rewrite-with-card-skimmer'
SCRIPT = 'objectives/supply-chain/hidden-payload/remote-loader::concealed-browser-script-source'
MODULE = 'objectives/supply-chain/hidden-payload/remote-loader::concealed-browser-module-source'
REMOTE_MODULE = 'micro-behaviors/os/module/require::dynamic-import-http-url'
REMOTE_SCRIPT = 'micro-behaviors/communications/http/client/script::js-remote-script-element'
FRAME = 'micro-behaviors/communications/http/client/frame::inserted-zero-size-offscreen-remote-iframe'
REVIEWED_COPY = 'objectives/impact/crypto-manipulation/hijack-transfer/address::browser-selected-wallet-copy-override'
REVIEWED_SOCKET = 'objectives/exfiltration/stealer/financial/payment-card::payment-input-websocket-value-flow'
REVIEWED_HTTPX = 'objectives/exfiltration/stealer/credential/environment/current-process::httpx-credential-env-values-concealed-upload'
CARGO_BODY = 'objectives/exfiltration/stealer/credential/file::rust-build-script-credential-http-body'
NPM_TOKEN = 'objectives/exfiltration/stealer/system-info/cloud-metadata::npm-preinstall-posts-gcp-metadata-token'
MAC_INSTALL = 'objectives/exfiltration/stealer/system-info/host-fingerprint::shell-macos-installer-fingerprint-exfil'


def wheel(name):
    return f'{name}-1.0-py3-none-any.whl'


def check_scan(atomscan, cases, paths):
    expected = {
        'wallet-and-card-module.js': 'block',
        'wallet-and-card-beacon.js': 'block',
        'wallet-and-card-websocket.js': 'block',
        'guarded-wallet-copy.js': 'block',
        'card-bound-websocket.js': 'block',
        'card-live-websocket.js': 'allow',
        'card-websocket-field-metadata.js': 'allow',
        'card-websocket-other-channel.js': 'allow',
        'card-websocket-checkout-submit.js': 'allow',
        'card-websocket-excluded-inputs.js': 'allow',
        'bound-httpx-alias.py': 'block',
        'concealed-httpx-alias.py': 'allow',
        'httpx-key-metadata.py': 'allow',
        'httpx-split-target-flow.py': 'allow',
        'guarded-wallet-copy-placeholder.js': 'allow',
        'npm-preinstall-gcp-metadata-token-exfil.zip': 'block',
        'build-report-hook.tgz': 'allow',
        'postinstall': 'block',
        'inventory.sh': 'allow',
        'cargo-startup-credential-flow/build.rs': 'block',
        'size-control/build.rs': 'allow',
        wheel('nested_startup'): 'block',
        wheel('requests'): 'block',
        wheel('httpx'): 'block',
        wheel('ordinary_hook'): 'allow',
        'wallet-copy-observer.js': 'allow',
        'card-live-fetch-metadata.js': 'allow',
        'card-live-fetch-unrelated.js': 'allow',
        'plain-module-import.js': 'allow',
        'separate-httpx.py': 'allow',
    }
    by_name = {
        f'{Path(relative).parent.name}/{path.name}' if path.name == 'build.rs' else path.name: path
        for (relative, _, _), path in zip(cases, paths)
    }
    for transport in ('beacon', 'websocket'):
        members = (
            by_name['wallet-copy-callback.js'],
            by_name[f'card-live-{transport}.js'],
            by_name['decoded-module-import.js'],
        )
        combined = members[0].with_name(f'wallet-and-card-{transport}.js')
        combined.write_text('\n'.join(member.read_text() for member in members))
        by_name[combined.name] = combined
    env = os.environ.copy()
    env.pop('SCAN_LLM', None)
    env.pop('SCAN_HOPPER', None)
    env.update(CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_ANALYSIS_CACHE='1', ATOMDRIFT_UPLINK='0')
    result = subprocess.run(
        [atomscan, '--offline', '--mode', 'slow', '--follow=none',
         '--format', 'json', *(str(by_name[name]) for name in expected)],
        cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
    )
    # 0 benign, 1 hostile, 2 suspicious; 3 and 4 mean the scan proves nothing.
    if result.returncode not in (0, 1, 2):
        raise SystemExit(f'atomscan exited with status {result.returncode}')
    observed = {
        Path(report['path']): report['decision']
        for report in map(json.loads, result.stdout.splitlines())
    }
    for name, decision in expected.items():
        actual = observed.get(by_name[name])
        if actual != decision:
            raise SystemExit(f'{name}: expected {decision}, got {actual}')
    print(f'Validated default Scan decisions for {len(expected)} supply-chain fixtures')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--atomscan', help='Also assert default policy block and allow decisions')
    args = parser.parse_args()
    incident_cases = [
        ('hostile', PYTHON, wheel('nested_startup'), {PTH, PROC, ENV, CI, IDENTITY}, set()),
        ('hostile', PYTHON, wheel('direct_startup'), {PTH, PROC, ENV, CI, IDENTITY}, set()),
        ('hostile', PYTHON, wheel('stdlib_positional'), {PTH, PROC}, set()),
        ('hostile', PYTHON, wheel('requests'), {PTH, PROC}, set()),
        ('hostile', PYTHON, wheel('httpx'), {PTH, PROC}, set()),
        ('hostile', PYTHON, wheel('sitecustomize'), {CUSTOMIZE, PROC}, {PTH}),
        ('hostile', PYTHON, wheel('usercustomize'), {CUSTOMIZE, PROC}, {PTH}),
        ('hostile', PYTHON, wheel('no_executable_hook'), {PROC}, {PTH, CUSTOMIZE}),
        ('suspicious', PYTHON, wheel('unrelated_members'), set(), {PTH, PROC}),
        ('suspicious', PYTHON, wheel('no_encoded_body'), set(), {PTH, PROC}),
        ('notable', PYTHON, wheel('ordinary_hook'), set(), {PTH, PROC}),
        ('hostile', PYTHON, 'concealed-httpx.py', {ENV}, {PTH, PROC}),
        ('hostile', PYTHON, 'concealed-httpx-alias.py', {ENV}, {PTH, PROC}),
        ('hostile', PYTHON, 'bound-httpx-alias.py', {REVIEWED_HTTPX}, {PTH, PROC}),
        ('hostile', PYTHON, 'httpx-key-metadata.py', {ENV}, {REVIEWED_HTTPX}),
        ('hostile', PYTHON, 'httpx-split-target-flow.py', {ENV}, {REVIEWED_HTTPX}),
        ('notable', PYTHON, 'relative-httpx-alias.py', set(), {ENV}),
        ('hostile', PYTHON, 'concealed-requests.py', {ENV}, {PTH, PROC}),
        ('notable', PYTHON, 'separate-httpx.py', set(), {ENV}),
        ('hostile', BROWSER, 'encoded-copy-hook.js', {ENCODED_COPY}, set()),
        ('hostile', BROWSER, 'wallet-copy-callback.js', {COPY}, set()),
        ('hostile', BROWSER, 'guarded-wallet-copy.js', {REVIEWED_COPY}, {COPY}),
        ('notable', BROWSER, 'guarded-wallet-copy-placeholder.js', set(), {REVIEWED_COPY}),
        ('hostile', BROWSER, 'card-fetch-hook.js', {CARD}, set()),
        ('hostile', BROWSER, 'card-live-websocket.js', {CARD_SOCKET}, {CARD, CARD_FETCH}),
        ('hostile', BROWSER, 'card-bound-websocket.js', {REVIEWED_SOCKET}, {CARD, CARD_SOCKET}),
        ('notable', BROWSER, 'card-websocket-field-metadata.js', set(), {REVIEWED_SOCKET}),
        ('notable', BROWSER, 'card-websocket-other-channel.js', set(), {REVIEWED_SOCKET}),
        ('notable', BROWSER, 'card-websocket-checkout-submit.js', set(), {REVIEWED_SOCKET}),
        ('notable', BROWSER, 'card-websocket-excluded-inputs.js', set(), {REVIEWED_SOCKET}),
        ('hostile', BROWSER, 'wallet-and-card-module.js', {COPY, CARD_FETCH, CARD_AND_COPY, MODULE}, set()),
        ('suspicious', BROWSER, 'card-live-beacon.js', {CARD_BEACON}, {CARD_AND_COPY}),
        ('suspicious', BROWSER, 'card-live-fetch.js', {CARD_FETCH}, {CARD, CARD_SOCKET}),
        ('suspicious', BROWSER, 'card-live-fetch.ts', {CARD_FETCH}, {CARD, CARD_SOCKET}),
        ('notable', BROWSER, 'card-live-fetch-metadata.js', set(), {CARD_FETCH}),
        ('notable', BROWSER, 'card-live-fetch-unrelated.js', set(), {CARD_FETCH}),
        ('suspicious', BROWSER, 'decoded-script-direct.js', {SCRIPT}, set()),
        ('suspicious', BROWSER, 'decoded-script-variable.js', {SCRIPT}, set()),
        ('suspicious', BROWSER, 'decoded-module-import.js', {MODULE}, set()),
        ('notable', BROWSER, 'plain-module-import.js', {REMOTE_MODULE}, {MODULE}),
        ('suspicious', BROWSER, 'concealed-frame.js', {FRAME}, set()),
        ('suspicious', BROWSER, 'encoded-clipboard-readonly.js', set(), {ENCODED_COPY}),
        ('notable', BROWSER, 'decoded-image.js', set(), {SCRIPT}),
        ('notable', BROWSER, 'plain-project-loader.js', {REMOTE_SCRIPT}, {SCRIPT}),
        ('notable', BROWSER, 'wallet-copy-observer.js', set(), {COPY, CARD_AND_COPY}),
        ('notable', BROWSER, 'card-preview-no-network-hook.js', set(), {CARD}),
    ]
    raw_dns = 'objectives/exfiltration/dns/lookup::raw-socket-dns-exfil'
    android_input = 'objectives/credential-access/capture/input::android-raw-touch-credential-reconstruction'
    zig_packages = 'testdata/hostile/generated/reduced/hostile/supply-chain-corpus/zig'
    android_hostile = 'testdata/hostile/hopper-triage/acquit-registry-loader-review'
    android_notable = 'testdata/notable/hopper-triage/acquit-registry-loader-review'
    cases = [
        (f'testdata/{severity}/generated/{category}/{name}', required, forbidden)
        for severity, category, name, required, forbidden in incident_cases
    ] + [
        ('testdata/hostile/generated/python-raw-dns-host-profile-exfil.py', {raw_dns}, set()),
        ('testdata/notable/controls/python-raw-dns-health-query.py', set(), {raw_dns}),
        ('testdata/hostile/controls/ps-dns-txt-chunk-exfil/chunked-file-exfil.ps1',
         {'objectives/exfiltration/dns/tunnel::ps-routeros-dns-c2-exfil'}, set()),
        ('testdata/hostile/node-telegram-env-session-exfil.js',
         {'objectives/exfiltration/stealer/configuration/environment/process::node-project-secret-telegram-upload'}, set()),
        ('testdata/hostile/npm-install-host-user-dns-exfil/package.json',
         {'objectives/exfiltration/stealer/system-info/process::npm-install-host-user-dns-exfil'}, set()),
        (f'{zig_packages}/zigpkg-marrowflow-whois-c2-envexfil-linux.tar.gz',
         {'objectives/exfiltration/stealer/credential/file::zig-build-credential-upload'}, set()),
        (f'{zig_packages}/zigpkg-marrowforge-clipboard-clipper-windows.tar.gz',
         {'objectives/impact/crypto-manipulation/clipboard::source-winforms-clipboard-address-clipper'}, set()),
        (f'{android_hostile}/android-raw-credential-flow.java', {android_input}, set()),
        (f'{android_notable}/android-unrelated-credential-flow.java', set(), {android_input}),
        ('testdata/hostile/generated/cargo-startup-credential-flow/build.rs', {CARGO_BODY}, set()),
        ('testdata/notable/generated/cargo-startup-credential-flow/size-control/build.rs', set(), {CARGO_BODY}),
        ('testdata/hostile/generated/npm-preinstall-gcp-metadata-token-exfil.zip', {NPM_TOKEN}, set()),
        ('testdata/notable/npm-install-hook-controls/build-report-hook.tgz', set(), {NPM_TOKEN}),
        ('testdata/hostile/generated/macos-installer-fingerprint-exfil/postinstall', {MAC_INSTALL}, set()),
        ('testdata/notable/generated/macos-installer-fingerprint-controls/inventory.sh', set(), {MAC_INSTALL}),
    ]
    with tempfile.TemporaryDirectory(prefix='cleave-supply-chain-') as directory:
        paths = []
        for index, (relative, _, _) in enumerate(cases):
            source = ROOT / relative
            case_dir = Path(directory) / str(index)
            case_dir.mkdir()
            paths.append(shutil.copyfile(source, case_dir / source.name))
        lines = subprocess.check_output(
            [args.cleave, '--traits-dir', str(ROOT), '--format', 'json', *paths],
            cwd=ROOT, text=True,
        )
        if args.atomscan:
            check_scan(args.atomscan, cases, paths)
    reports = {}
    for line in lines.splitlines():
        files = json.loads(line)['files']
        reports[Path(files[0]['path'])] = {
            trait['id']: trait['crit'] for member in files for trait in member.get('traits', [])
        }
    for (name, required, forbidden), path in zip(cases, paths):
        findings = reports[path]
        found = findings.keys()
        if path.name == 'guarded-wallet-copy.js':
            hostile = {trait for trait, severity in findings.items() if severity == 5}
            if hostile != {REVIEWED_COPY}:
                raise SystemExit(f'{name}: expected one reviewed hostile trait, got {sorted(hostile)}')
        if missing := required - found:
            raise SystemExit(f'{name}: missing {", ".join(sorted(missing))}')
        if unexpected := forbidden & found:
            raise SystemExit(f'{name}: unexpected {", ".join(sorted(unexpected))}')
    print(f'Validated trait expectations for {len(cases)} supply-chain fixtures')


if __name__ == '__main__':
    main()
