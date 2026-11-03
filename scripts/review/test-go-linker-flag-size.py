#!/usr/bin/env python3
"""Ensure linker flag evidence does not disappear in large build scripts."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
RULE = 'metadata/build/compiler::go-ldflags-strip'

with tempfile.TemporaryDirectory(prefix='go-linker-flags-') as temp:
    root = Path(temp)
    dest = root / 'rules/metadata/build/compiler/traits.yaml'
    dest.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'metadata/build/compiler/toolchain-review-go-options.yaml', dest)
    cases = (
        ('small', 'go build -ldflags "-s -w" ./cmd\n', True),
        ('large', '# padding\n' * 700 + 'go build -ldflags "-s -w" ./cmd\n', True),
        ('other', 'go build -ldflags "-w" ./cmd\n', False),
    )
    for name, content, expected in cases:
        sample = root / (name + '.sh')
        sample.write_text(content)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(root / 'rules'),
                                 'test-rules', '--rules', RULE, str(sample)],
                                check=True, capture_output=True, text=True)
        status = 'MATCHED ' if expected else 'NOT MATCHED '
        if '\n' + status + RULE + ' ' not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
