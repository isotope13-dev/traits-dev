"""A bundler-inlined version stamp is not property-concat obfuscation.

Run: python3 testdata/property-concat-version-stamp/verify.py <scratch-dir>

Bundlers inline `require('../package.json').version` as
`{version: "6.5.4"}.version` (as in the elliptic copy inside ethers'
dist bundle). The dotted-numeric value is a version stamp, not a
recovered string. An inline object access recovering a URL must still
report `js-property-concatenation-obfuscation`.

Fixture sources are copied to the scratch directory because the trait
suppresses anything under a test path.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TRAIT = ('objectives/anti-static/obfuscation/syntax::'
         'js-property-concatenation-obfuscation')


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

    benign = dest / 'version-stamp.js'
    shutil.copyfile(HERE / 'version-stamp.js', benign)
    assert TRAIT not in scan(benign), 'version stamp must not fire'
    print('PASS version-stamp.js', flush=True)

    hostile = dest / 'string-recovery.js'
    shutil.copyfile(HERE / 'string-recovery.js', hostile)
    assert TRAIT in scan(hostile), 'recovered URL string must fire'
    print('PASS string-recovery.js', flush=True)


if __name__ == '__main__':
    main()
