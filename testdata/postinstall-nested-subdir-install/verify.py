"""Nested subdir bare install is not a consumer-project injection.

Run: python3 testdata/postinstall-nested-subdir-install/verify.py <scratch-directory>

Pre-flat-install packages (MeanJS-era) keep a nested package.json and
install it from postinstall with `cd ./subdir && npm install && cd
../..`. The trailing ascent matches the parent-directory-escape text,
but it only undoes the descent, and a bare `npm install` names no
package to inject -- unlike `cd ../../.. && npm install evil`, which
lands in the consumer project with an undeclared dependency and must
still convict.

Controls: a package.json whose postinstall escapes to the consumer and
installs a named package must report
`install-hook-injects-consumer-dependency`; the nested bare-install
shape must report neither the hostile nor the escape/install
suspicious traits; the nested shape with a named package must keep its
suspicious traits (and the hostile, which still sees both legs).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOSTILE = ('objectives/supply-chain/install-hook/project-rewrite::'
           'install-hook-injects-consumer-dependency')
ESCAPE = ('objectives/supply-chain/install-hook/project-rewrite::'
          'install-hook-parent-directory-escape')
PKG_INSTALL = ('objectives/supply-chain/install-hook/package/manifest::'
               'install-hook-runs-pkg-install')

POSITIVE = {'scripts': {'postinstall': 'cd ../../.. && npm install evil'}}
NEGATIVE = {'scripts': {'postinstall':
                        'cd ./lib/core_modules/server && npm install && cd ../../..'}}
NAMED_NESTED = {'scripts': {'postinstall':
                            'cd ./lib && npm install evil && cd ../..'}}


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry['traits']}


def write_manifest(dest, name, manifest):
    sub = dest / name
    sub.mkdir(parents=True, exist_ok=True)
    path = sub / 'package.json'
    path.write_text(json.dumps(manifest))
    return path


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    ids = scan(write_manifest(dest, 'positive', POSITIVE))
    assert HOSTILE in ids, 'consumer escape plus named install must convict'
    print('PASS positive/package.json', flush=True)

    ids = scan(write_manifest(dest, 'negative', NEGATIVE))
    assert HOSTILE not in ids, 'nested bare install must not convict'
    assert ESCAPE not in ids, 'balanced return is not an escape'
    assert PKG_INSTALL not in ids, 'bare self-install is not injection'
    print('PASS negative/package.json', flush=True)

    ids = scan(write_manifest(dest, 'named-nested', NAMED_NESTED))
    assert HOSTILE in ids, 'nested named install must still convict'
    print('PASS named-nested/package.json', flush=True)


if __name__ == '__main__':
    main()
