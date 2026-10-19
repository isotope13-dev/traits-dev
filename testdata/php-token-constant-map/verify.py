"""A field mapped to a constant name is not a hardcoded token.

Run: python3 testdata/php-token-constant-map/verify.py <scratch-dir>

Storage SDKs map settings fields to deployment constants
(`'api_key' => 'ACME_STORAGE_API_KEY'`); the constant's value comes from
site configuration, so the uppercase identifier is a reference, not a
secret. A contiguous random-looking token value must still report
`php-hardcoded-token-field`.

Fixture sources are copied to the scratch directory because traits in
this family suppress anything under a test path.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TRAIT = ('micro-behaviors/communications/http/request/credentials::'
         'php-hardcoded-token-field')


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

    benign = dest / 'constant-map.php'
    shutil.copyfile(HERE / 'constant-map.php', benign)
    assert TRAIT not in scan(benign), 'constant-name value must not fire'
    print('PASS constant-map.php', flush=True)

    hostile = dest / 'hardcoded-token.php'
    shutil.copyfile(HERE / 'hardcoded-token.php', hostile)
    assert TRAIT in scan(hostile), 'hardcoded token value must fire'
    print('PASS hardcoded-token.php', flush=True)


if __name__ == '__main__':
    main()
