#!/usr/bin/env python3
"""Check both legs of the Xcode build-context exclusion."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
RULE = 'metadata/build/xcode::xcode-platform-args-build-context'

with tempfile.TemporaryDirectory(prefix='xcode-context-') as temp:
    root = Path(temp)
    dest = root / 'rules/metadata/build/xcode/context.yaml'
    dest.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'metadata/build/xcode/context.yaml', dest)
    cases = (
        ('both', 'command = "xcrun -sdk macosx clang"\noutput = "DERIVED_FILES_DIR"\n', True),
        ('no-output', 'command = "xcrun -sdk macosx clang"\n', False),
        ('no-compiler', 'output = "DERIVED_FILES_DIR"\n', False),
    )
    for name, content, expected in cases:
        sample = root / (name + '.py')
        sample.write_text(content)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(root / 'rules'),
                                 'test-rules', '--rules', RULE, str(sample)],
                                check=True, capture_output=True, text=True)
        status = 'MATCHED ' if expected else 'NOT MATCHED '
        if '\n' + status + RULE + ' ' not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
