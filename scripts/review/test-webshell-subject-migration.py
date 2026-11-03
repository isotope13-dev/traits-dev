#!/usr/bin/env python3
"""Request-fed command evidence must not depend on arbitrary file size."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/command-and-control/backdoor/webshell/command::post-command-passthru'
with tempfile.TemporaryDirectory(prefix='request-sink-') as tmp:
    for name, content, expected in (
        ('small.php', "<?php passthru($_POST['cmd']); ?>\n", 'MATCHED'),
        ('large.php', "<?php passthru($_POST['cmd']); ?>\n" + (' ' * 60000), 'MATCHED'),
        ('ordinary.php', "<?php passthru('date'); ?>\n", 'NOT MATCHED'),
    ):
        path = Path(tmp) / name
        path.write_text(content)
        trace = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(path)], text=True, capture_output=True, check=True).stdout
        assert f'{expected} {RULE}' in trace, trace
print('Request-fed command: small, large and ordinary-command cases passed')
