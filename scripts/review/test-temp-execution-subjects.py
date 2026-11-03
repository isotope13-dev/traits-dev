#!/usr/bin/env python3
"""Check temporary script sourcing and chmod clues after migration."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
SOURCE = 'micro-behaviors/process/interpreter/shell::executes-tmp-file-source'
CHMOD = 'micro-behaviors/fs/chmod/executable/mode::android-tmp-chmod-path-clues'
CASES = (
    ('source.sh', 'source /tmp/loader.sh\n', SOURCE, 'MATCHED'),
    ('mention.sh', 'echo /tmp/loader.sh\n', SOURCE, 'NOT MATCHED'),
    ('chmod.sh', 'chmod +x /data/local/tmp/a; /data/local/tmp/b\n', CHMOD, 'MATCHED'),
    ('path.sh', 'echo /data/local/tmp/a /data/local/tmp/b\n', CHMOD, 'NOT MATCHED'),
)
with tempfile.TemporaryDirectory(prefix='temp-subjects-') as tmp:
    for name, content, rule, expected in CASES:
        path = Path(tmp) / name
        path.write_text(content)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', rule, str(path)], text=True, capture_output=True, check=True)
        assert f'{expected} {rule}' in result.stdout, result.stdout + result.stderr
print('Temporary source and chmod clues: positive and near-miss cases passed')
