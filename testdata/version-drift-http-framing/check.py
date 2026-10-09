"""Verify framing and identity controls outside the test-directory exclusion."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

fixtures = Path(__file__).resolve().parent
framing = 'objectives/execution/exploit/http-desync::duplicate-content-length-http-desync-source'
accept = 'objectives/evasion/security-bypass/auth::rust-zero-identity-acceptance'
comparison = 'micro-behaviors/data/control-flow/branch::rust-zero-six-byte-or-comparison'
cases = {
    'probe.rs': (set(), {framing}),
    'pipeline.rs': ({framing}, set()),
    'reject-zero.rs': ({comparison}, {accept}),
    'accept-zero.rs': ({comparison, accept}, set()),
}
with tempfile.TemporaryDirectory(prefix='drift-controls-') as directory:
    for name, (required, forbidden) in cases.items():
        target = Path(directory) / name
        shutil.copyfile(fixtures / name, target)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--format', 'jsonl', str(target)],
            env={**os.environ, 'CLEAVE_VALIDATE': '0'},
            check=True, capture_output=True, text=True,
        )
        ids = {trait['id'] for line in result.stdout.splitlines()
               for file in json.loads(line).get('files', [])
               for trait in file.get('traits', [])}
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        print(name, 'passed')
