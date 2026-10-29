#!/usr/bin/env python3
"""Allocating RWX memory is distinct from changing existing protection."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
ALLOC = 'micro-behaviors/mem/alloc/virtual::powershell-virtualalloc-rwx-argument'
PROTECT = 'micro-behaviors/mem/protect/modify/executable::powershell-virtualprotect-rwx-argument'
CASES = [
    ('allocation', 'VirtualAlloc(0, 4096, 0x3000, 0x40)', True, False),
    ('protection', 'VirtualProtect(0, 4096, 0x40, $old)', False, True),
]
with tempfile.TemporaryDirectory(prefix='memory-protection-boundary-') as directory:
    for name, code, alloc, protect in CASES:
        target = Path(directory) / (name + '.ps1')
        target.write_text(code + '\n' + '# padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', ALLOC + ',' + PROTECT], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule, expected in ((ALLOC, alloc), (PROTECT, protect)):
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
