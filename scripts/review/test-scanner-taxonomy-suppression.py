#!/usr/bin/env python3
"""Keep the reviewed security-scanner exclusion narrower than scanner profiles."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='scanner-taxonomy-') as tmp:
    root = Path(tmp)
    sql = ('sql = "CREATE TABLE secrets (provider TEXT, secret TEXT, '
           'source_url TEXT, status TEXT)"\nstates = "unchecked valid invalid"\n')
    cases = {
        'neutral.py': sql,
        'security.py': sql + 'doc = "scanner module for detecting security risks"\n',
        'threat.py': sql + 'MINING_SIGNATURES = []\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    inventory = 'micro-behaviors/data/db/schema/relational::secret-validation-inventory-schema'
    security = 'metadata/file/profile/scanner/security::defensive-security-scanner-module-doc'
    threat = 'metadata/file/profile/scanner/threat::defensive-threat-signatures'
    assert inventory in ids['neutral.py'] and inventory in ids['threat.py']
    assert security in ids['security.py'] and inventory not in ids['security.py']
    assert threat in ids['threat.py'] and security not in ids['threat.py']
    print('The security-scanner exclusion retains its original narrow scope.')
