#!/usr/bin/env python3
"""A command fragment must not suppress itself as command-policy evidence."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
POLICY = 'micro-behaviors/os/security/command-policy::command-policy-implementation-context'
COMMAND = 'micro-behaviors/fs/delete/directory::root-deletion-command-reference'
CASES = (
    ('command.sh', '#!/bin/sh\nrm -rf / --no-preserve-root\n', False, True),
    ('guard.sh', '#!/bin/sh\nBLOCKED_PATTERNS=(\'rm -rf / --no-preserve-root\')\nprintf \'{"decision":"deny"}\\n\'\n', True, False),
    ('guard.py', 'import re\nclass Policy:\n    def check(self, command):\n        for pattern in self.denylist:\n            if re.search(pattern, command):\n                return Decision(allowed=False)\n', True, None),
)

# Scan source only. Never execute the synthetic command or policy samples.
# Avoid "test"/"fixture" path components: they would independently suppress it.
with tempfile.TemporaryDirectory(prefix='process-policy-probe-') as directory:
    for name, source, policy_expected, command_expected in CASES:
        path = Path(directory) / name
        path.write_text(source)
        expected = [(POLICY, policy_expected)]
        if command_expected is not None:
            expected.append((COMMAND, command_expected))
        result = subprocess.run(
            [CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(path),
             '--rules', ','.join(rule for rule, _ in expected)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        lines = result.stdout.splitlines()
        for rule, matches in expected:
            prefix = ('MATCHED ' if matches else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in lines), (name, prefix, result.stdout)
        if name == 'guard.sh':
            assert 'Skipped by' in result.stdout and 'command-policy-implementation-context' in result.stdout
        print(f'{name}: passed')
