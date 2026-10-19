"""A root *.js files-glob ships the companion loader it names.

Run: python3 testdata/install-hook-companion-glob/verify.py <scratch-dir>

Manifests whose `files` allowlist is a root JavaScript glob
(`*.{js,d.ts}`, `*.js`) ship every root loader the hook can name, so
`postinstall: node postinstall.js` is not a dead hook. A hook naming a
loader the allowlist does not cover must still report
`install-hook-missing-companion-loader`.

Manifests are staged as package.json in the scratch directory because
the pairing is file-scoped and traits suppress test paths.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TRAIT = ('objectives/supply-chain/install-hook/scripts/local-script::'
         'install-hook-missing-companion-loader')


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry.get('traits', [])}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    benign = dest / 'glob' / 'package.json'
    benign.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / 'glob-manifest.json', benign)
    assert TRAIT not in scan(benign), 'root *.js glob must not fire'
    print('PASS glob', flush=True)

    hostile = dest / 'missing' / 'package.json'
    hostile.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / 'missing-manifest.json', hostile)
    assert TRAIT in scan(hostile), 'uncovered loader must fire'
    print('PASS missing', flush=True)


if __name__ == '__main__':
    main()
