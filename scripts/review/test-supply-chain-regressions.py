#!/usr/bin/env python3
"""Assert the individual traits behind representative supply-chain findings."""

import argparse
import json
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
SCRIPT = 'objectives/supply-chain/hidden-payload/remote-loader::concealed-browser-script-source'
REMOTE_SCRIPT = 'micro-behaviors/communications/http/client/script::js-remote-script-element'
FRAME = 'micro-behaviors/communications/http/client/frame::inserted-zero-size-offscreen-remote-iframe'


def wheel(name):
    return f'{name}-1.0-py3-none-any.whl'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    cases = [
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
        ('hostile', BROWSER, 'encoded-copy-hook.js', {ENCODED_COPY}, set()),
        ('hostile', BROWSER, 'wallet-copy-callback.js', {COPY}, set()),
        ('hostile', BROWSER, 'card-fetch-hook.js', {CARD}, set()),
        ('suspicious', BROWSER, 'decoded-script-direct.js', {SCRIPT}, set()),
        ('suspicious', BROWSER, 'decoded-script-variable.js', {SCRIPT}, set()),
        ('suspicious', BROWSER, 'concealed-frame.js', {FRAME}, set()),
        ('suspicious', BROWSER, 'encoded-clipboard-readonly.js', set(), {ENCODED_COPY}),
        ('notable', BROWSER, 'decoded-image.js', set(), {SCRIPT}),
        ('notable', BROWSER, 'plain-project-loader.js', {REMOTE_SCRIPT}, {SCRIPT}),
        ('notable', BROWSER, 'wallet-copy-observer.js', set(), {COPY}),
        ('notable', BROWSER, 'card-preview-no-network-hook.js', set(), {CARD}),
    ]
    with tempfile.TemporaryDirectory(prefix='cleave-supply-chain-') as directory:
        paths = []
        for severity, category, name, _, _ in cases:
            source = ROOT / 'testdata' / severity / 'generated' / category / name
            paths.append(shutil.copyfile(source, Path(directory) / name))
        lines = subprocess.check_output(
            [args.cleave, '--traits-dir', str(ROOT), '--format', 'json', *paths],
            cwd=ROOT, text=True,
        )
    reports = {}
    for line in lines.splitlines():
        files = json.loads(line)['files']
        reports[Path(files[0]['path']).name] = {
            trait['id'] for member in files for trait in member.get('traits', [])
        }
    for _, _, name, required, forbidden in cases:
        found = reports[name]
        if missing := required - found:
            raise SystemExit(f'{name}: missing {", ".join(sorted(missing))}')
        if unexpected := forbidden & found:
            raise SystemExit(f'{name}: unexpected {", ".join(sorted(unexpected))}')
    print(f'Validated trait expectations for {len(cases)} supply-chain fixtures')


if __name__ == '__main__':
    main()
