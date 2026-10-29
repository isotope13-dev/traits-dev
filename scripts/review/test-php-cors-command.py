#!/usr/bin/env python3
"""CORS headers cannot suppress an independently request-controlled command."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
COMMAND = 'micro-behaviors/process/create/shell/request::exec-user-input'
CORS = 'metadata/file/profile/operation-reference::extension-origin-post-cors-reference'
WEBSHELL = 'objectives/command-and-control/backdoor/webshell/request/command::php-shell-post'
HEADERS = 'header("Access-Control-Allow-Origin: chrome-extension://example");\nheader("Access-Control-Allow-Methods: POST");\n'
CASES = [('cors-command', HEADERS + 'system($_POST["cmd"]);\n', True, True),
         ('cors-only', HEADERS + 'echo "ok";\n', True, False),
         ('command-only', 'system($_POST["cmd"]);\n', False, True)]
with tempfile.TemporaryDirectory(prefix='php-cors-command-') as directory:
    for name, body, cors, command in CASES:
        target = Path(directory) / (name + '.php')
        target.write_text('<?php\n' + body + '?>\n' + '<!-- padding -->\n' * 70)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', ','.join([CORS, COMMAND, WEBSHELL])], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule, expected in ((CORS, cors), (COMMAND, command), (WEBSHELL, command)):
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, rule, result.stdout)
        print(name + ': passed', flush=True)
