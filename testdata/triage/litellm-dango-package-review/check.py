#!/usr/bin/env python3
"""Static source-form controls and the existing real PHP smoke-test fixture."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = {
    HERE / 'source-forms.js': {
        'metadata/lang/source/literal::js-single-lowercase-token-line',
        'micro-behaviors/hardware/input/mouse/message::mouseclick-event-name-literal',
        'metadata/lang/source/syntax/call/arguments::js-token-save-mutation-call-text',
        'metadata/lang/natural/phrasing::discord-user-token-tos-disclosure',
    },
    HERE / 'source-forms.py': {
        'metadata/lang/source/literal::victim-command-session-wording',
        'metadata/lang/source/literal::api-key-label-near-hex-string',
        'metadata/lang/natural/phrasing::secret-acquisition-wording',
        'metadata/lang/source/naming/setting::python-verification-skip-name',
        'metadata/lang/source/shape::python-verification-skip-name-with-getenv',
        'metadata/lang/source/declaration::python-optional-callback-url-field',
    },
    HERE / 'user-location.rs': {
        'metadata/lang/source/naming/setting::quoted-user-location-field-name',
    },
    ROOT / 'testdata/benign/shell-php-smoke-test/smoke.sh': {
        'micro-behaviors/process/create/shell/stdin-feed::php-snippet-piped-into-php-stdin',
    },
}

def main():
    binary = os.environ.get('CLEAVE', 'cleave')
    proc = subprocess.run([binary, '--traits-dir', str(ROOT), '--format', 'json',
                           *map(str, CASES)], capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    rest = proc.stdout.strip()
    files = []
    while rest:
        report, end = decoder.raw_decode(rest)
        files.extend(report['files'])
        rest = rest[end:].lstrip()
    for path, expected in CASES.items():
        f = next(f for f in files if Path(f['path']).resolve() == path.resolve())
        ids = {t['id'] for t in f.get('traits', [])}
        assert expected <= ids, (path.name, sorted(expected - ids))
        assert not [t for t in f.get('traits', []) if t['crit'] >= 4], path.name
        if path.name == 'source-forms.js':
            assert 'micro-behaviors/process/create/shell/stdin-feed::php-snippet-piped-into-php-stdin' not in ids
        assert 'objectives/persistence/login/shell/profile::node-shell-rc-command-persistence' not in ids
    print('PASS: all 11 relocated observations, PHP pipeline retention, and actual benign near misses')

if __name__ == '__main__':
    main()
