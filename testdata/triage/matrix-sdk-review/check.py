"""Precision controls for API comments and whole-module re-exports.

Run with CLEAVE pointing to the selected engine. No fixture is executed.
"""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'micro-behaviors/data/control-flow/module-exec::'
SOLE = PREFIX + 'sole-require-passthrough-module'
PACKAGE = PREFIX + 'sole-package-require-passthrough'
EXPORT = PREFIX + 'commonjs-export-require-expression'
REQUEST = 'objectives/impact/ransom/encrypt/threat-text::encrypt-decryptor-msg-2'
LOADER = 'objectives/supply-chain/hidden-payload/remote-loader::'


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)['files']


def check(path, required=(), forbidden=()):
    files = scan(path)
    traits = {t['id'] for f in files for t in f.get('traits', [])}
    assert set(required) <= traits, (path.name, 'missing', set(required) - traits)
    assert not set(forbidden) & traits, (path.name, 'unexpected', set(forbidden) & traits)
    print('PASS', path.name)
    return files


def main():
    check(HERE / 'api-comment.js', forbidden=[REQUEST])
    check(HERE / 'ransom-literal.js', required=[REQUEST])
    check(HERE / 'commented-passthrough.js', required=[SOLE, PACKAGE, EXPORT])
    check(HERE / 'relative-passthrough.js', required=[SOLE, EXPORT], forbidden=[PACKAGE])
    for name in ['bundle-reexport.js', 'extra-logic.js', 'quoted-passthrough.js']:
        check(HERE / name, required=[EXPORT], forbidden=[SOLE, PACKAGE])
    check(ROOT / 'testdata/suspicious/version-drift-collector-npm/survey-client-10.0.12.tgz',
          required=[SOLE, PACKAGE, LOADER + 'hollow-entry-reexports-remote-url-dep',
                    LOADER + 'sole-mutable-url-dependency-reexport'])
    files = check(ROOT / 'testdata/hostile/grabvy-fernet-ransomware.py', required=[
        'objectives/impact/ransom/encrypt/filesystem::python-fernet-walk-encrypt-delete-original',
        'objectives/impact/ransom/encrypt-note::ransom-note-with-walk-encryption'])
    assert sum(t['crit'] == 5 for f in files for t in f['traits']) >= 2


if __name__ == '__main__':
    main()
