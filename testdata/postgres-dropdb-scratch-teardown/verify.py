"""Scratch databases created and dropped in one script are not destruction.

Run: python3 testdata/postgres-dropdb-scratch-teardown/verify.py <scratch-dir>

A benchmark harness (e.g. pg_sift bench/steps/cpu_gate.sh) starts its own
cluster, makes template databases with SQL CREATE DATABASE, copies one per
measured cell, and drops each copy afterwards. That teardown must not
report `postgres-dropdb-command`. Dropping a database the script never
created must still report it.

Fixtures are written to the scratch directory, not testdata/, because the
trait already suppresses anything under a test path.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRAIT = 'objectives/impact/destroy/database::postgres-dropdb-command'

BENIGN = """#!/bin/sh
psql -c "CREATE DATABASE bench_scratch TEMPLATE template0"
psql -c "CREATE DATABASE bench_cell TEMPLATE bench_scratch"
dropdb bench_cell
dropdb bench_scratch
"""
HOSTILE = "#!/bin/sh\ndropdb production\n"


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

    benign = dest / 'teardown.sh'
    benign.write_text(BENIGN)
    assert TRAIT not in scan(benign), 'scratch created-and-dropped must not fire'
    print('PASS teardown.sh', flush=True)

    hostile = dest / 'drop-production.sh'
    hostile.write_text(HOSTILE)
    assert TRAIT in scan(hostile), 'dropping an uncreated database must fire'
    print('PASS drop-production.sh', flush=True)


if __name__ == '__main__':
    main()
