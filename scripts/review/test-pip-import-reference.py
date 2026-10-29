#!/usr/bin/env python3
"""A pip import reference must not match the prefix of another module name."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'metadata/import/package::python-pip-module-import'
with tempfile.TemporaryDirectory(prefix='pip-import-probe-') as directory:
    for name, statement, matches in [('pip', 'import pip', True), ('pipeline', 'import pipeline', False)]:
        target = Path(directory) / (name + '.py')
        target.write_text(statement + '\n#' + ' padding' * 90 + '\n')
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', RULE], cwd=ROOT, capture_output=True, text=True, check=True)
        prefix = ('MATCHED ' if matches else 'NOT MATCHED ') + RULE + ' '
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
