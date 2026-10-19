"""A /debug call on a loopback-owned server is not remote probing.

Run: python3 testdata/debug-endpoint-loopback/verify.py <scratch-dir>

Benchmark harnesses start their own server on 127.0.0.1 and call its
/debug/maintain endpoint through a base-address variable, so the
loopback literal sits in a different statement than the call. A probe
of a remote host's /debug page must still report
`python-debug-endpoint-http-probe-debug`.

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
TRAIT = ('objectives/discovery/network/scan/http::'
         'python-debug-endpoint-http-probe-debug')


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

    benign = dest / 'loopback-benchmark.py'
    shutil.copyfile(HERE / 'loopback-benchmark.py', benign)
    assert TRAIT not in scan(benign), 'loopback-owned server must not fire'
    print('PASS loopback-benchmark.py', flush=True)

    hostile = dest / 'remote-probe.py'
    shutil.copyfile(HERE / 'remote-probe.py', hostile)
    assert TRAIT in scan(hostile), 'remote /debug probe must fire'
    print('PASS remote-probe.py', flush=True)


if __name__ == '__main__':
    main()
