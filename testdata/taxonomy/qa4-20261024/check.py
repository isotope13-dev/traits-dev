#!/usr/bin/env python3
"""Check source-to-execution bindings and the QA4 false-positive controls."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
BOUND = 'objectives/execution/payload/script-eval::xor-blockchain-helper-'
GATE = 'objectives/anti-analysis/debugger-detect/combined-checks::native-clr-profiler-pointer-gate'


def documents(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            break
        value, offset = decoder.raw_decode(text, offset)
        yield value


def check(text):
    files = {Path(d['files'][0]['path']).name: d['files'][0]
             for d in documents(text)}
    for name in ['blockchain-code.js', 'recovered-loader.js', 'concealed-loader.tgz']:
        hostile = {t['id'] for t in files[name]['traits'] if t['crit'] == 5}
        assert {BOUND + 'result-eval', BOUND + 'detached-node-eval'} <= hostile, (name, hostile)
    for name in ['wallet-rpc-with-unrelated-eval.js', 'mismatched-code-variable.js',
                 'wallet-error.js', 'password-label.js', 'parked-domain.html', 'phone-login.php']:
        assert not [t for t in files[name]['traits'] if t['crit'] == 5], name
    for name in ['wallet-rpc-with-unrelated-eval.js', 'mismatched-code-variable.js']:
        assert not [t for t in files[name]['traits'] if t['id'].startswith(BOUND)], name
    for name in ['wallet-error.js', 'password-label.js', 'parked-domain.html', 'phone-login.php']:
        assert not [t for t in files[name]['traits'] if t['crit'] >= 4], name
    labels = {t['id'] for t in files['password-label.js']['traits']}
    assert 'micro-behaviors/data/format/credentials::password-labelled-value-concatenation' in labels
    assert 'micro-behaviors/data/format/credentials::password-labelled-value-concatenation' not in {t['id'] for t in files['wallet-error.js']['traits']}
    assert GATE not in {t['id'] for t in files['overlay-data.exe']['traits']}
    phone = {t['id'] for t in files['phone-login.php']['traits']}
    assert 'micro-behaviors/os/security/auth/session::symfony-request-account-stored-password-session' in phone
    print(f'QA4: {len(files)} regression cases passed')


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        check(Path(sys.argv[1]).read_text())
    else:
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json',
                                 'analyze', str(HERE)], check=True, capture_output=True, text=True)
        check(result.stdout)
