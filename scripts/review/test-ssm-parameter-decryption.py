#!/usr/bin/env python3
"""SSM decryption options must belong to the matched command object."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/communications/http/services/aws-ssm::ssm-decrypted-parameter-read'
CASES = {
    'singular': ('new GetParameterCommand({ Name: key, WithDecryption: true });', True),
    'plural': ('new GetParametersCommand({ Names: keys, WithDecryption: true });', True),
    'disabled': ('new GetParameterCommand({ Name: key, WithDecryption: false });', False),
    'other-object': ('new GetParameterCommand({ Name: key }); const x = { WithDecryption: true };', False),
    'other-command': ('new OtherCommand({ Name: key, WithDecryption: true });', False),
}
with tempfile.TemporaryDirectory(prefix='ssm-decrypt-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.js')
        path.write_text(source + '\n')
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        found = any(trait['id'] == RULE for trait in report.get('traits', []))
        assert found == CASES[name][1], (name, found, CASES[name][1])
print('SSM decryption observation binds the command object text')
