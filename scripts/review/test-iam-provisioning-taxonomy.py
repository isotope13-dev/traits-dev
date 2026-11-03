#!/usr/bin/env python3
"""Check IAM provisioning evidence without treating a policy update as a backdoor."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='iam-provisioning-') as tmp:
    root = Path(tmp)
    setup = "<?php\n$iam->createUser(['UserName' => 'alice']);\n$iam->createAccessKey(['UserName' => 'alice']);\n"
    cases = {'policy.php': setup + "$iam->updateAccountPasswordPolicy(['MinimumPasswordLength' => 16]);\n",
             'user-key.php': setup}
    for name, content in cases.items():
        (root / name).write_text(content)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    trait = 'micro-behaviors/communications/http/services/aws-iam::aws-iam-user-key-control-changes'
    assert trait in ids['policy.php'], ids['policy.php']
    assert trait not in ids['user-key.php']
    assert not any('aws-iam-backdoor-account-chain' in t for t in ids['policy.php'])
    print('IAM account and policy provisioning stays distinct from a backdoor claim.')
