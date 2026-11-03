#!/usr/bin/env python3
"""A hidden WSH launch remains detectable after unrelated file padding."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
RULE = 'micro-behaviors/process/create/hidden::wsh-hidden-async-run'

with tempfile.TemporaryDirectory(prefix='wsh-hidden-offset-') as temp:
    root = Path(temp)
    dest = root / 'rules/micro-behaviors/process/create/hidden/traits.yaml'
    dest.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'micro-behaviors/process/create/hidden/boundary-create-flags-wsh-async.yaml', dest)
    launch = 'CreateObject("WScript.Shell").Run "cmd.exe /c echo ok", 0, False\n'
    cases = (
        ('early', launch, True),
        ('late', "' unrelated filler\n" * 500 + launch, True),
        ('visible', 'CreateObject("WScript.Shell").Run "cmd.exe /c echo ok", 1, False\n', False),
        ('waiting', 'CreateObject("WScript.Shell").Run "cmd.exe /c echo ok", 0, True\n', False),
    )
    for name, content, expected in cases:
        sample = root / (name + '.vbs')
        sample.write_text(content)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(root / 'rules'),
                                 'test-rules', '--rules', RULE, str(sample)],
                                check=True, capture_output=True, text=True)
        status = 'MATCHED ' if expected else 'NOT MATCHED '
        if '\n' + status + RULE + ' ' not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
