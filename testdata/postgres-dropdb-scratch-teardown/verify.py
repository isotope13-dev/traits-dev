"""Preserve database operations without inferring destructive intent.

Run: python3 testdata/postgres-dropdb-scratch-teardown/verify.py <scratch-dir>

A benchmark harness (e.g. pg_sift bench/steps/cpu_gate.sh) starts its own
cluster, makes template databases with SQL CREATE DATABASE, copies one per
measured cell, and drops each copy afterwards. Both that teardown and a
standalone drop retain the notable schema-deletion capability. Creation of
an unrelated database must not hide a drop of a different database.

Fixtures are written to scratch so their content can be tested independently
of test-path metadata. No database commands are executed.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = 'objectives/impact/destroy/database::postgres-dropdb-command'
DROP = 'micro-behaviors/data/db/schema/delete::postgres-dropdb-command'
CREATE = 'micro-behaviors/data/db/schema/relational::postgres-createdb-command'

BENIGN = """#!/bin/sh
psql -c "CREATE DATABASE bench_scratch TEMPLATE template0"
psql -c "CREATE DATABASE bench_cell TEMPLATE bench_scratch"
dropdb bench_cell
dropdb bench_scratch
"""
STANDALONE = "#!/bin/sh\ndropdb production\n"


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id']: t['crit'] for entry in report['files']
            for t in entry.get('traits', [])}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    cases = [
        ('teardown.sh', BENIGN, {DROP}),
        ('drop-production.sh', STANDALONE, {DROP}),
        ('create-unrelated.sh', '#!/bin/sh\ncreatedb scratch\ndropdb production\n',
         {CREATE, DROP}),
        ('create-only.sh', '#!/bin/sh\ncreatedb scratch\n', {CREATE}),
        ('split-step.sh', 'dropdb --if-exists "$CI_DB_NAME"', {DROP}),
        ('native-command.ps1', 'dropdb --if-exists production\n', {DROP}),
        ('mention.sh', '#!/bin/sh\necho "dropdb production"\n# createdb scratch\n',
         set()),
        ('prefix.sh', '#!/bin/sh\ndropdb_helper production\ncreatedb_helper scratch\n',
         set()),
    ]
    for name, source, expected in cases:
        path = dest / name
        path.write_text(source)
        traits = scan(path)
        assert OLD not in traits, (name, 'generic CLI is not an objective')
        assert {DROP, CREATE}.intersection(traits) == expected, (name, traits)
        assert all(traits[t] == 3 for t in expected), (name, traits)
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
