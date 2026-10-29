#!/usr/bin/env python3
"""Saving an existing capture does not establish screen acquisition."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
CAPTURE = 'micro-behaviors/hardware/display/screenshot::go-screenshot-capture-call'
REFERENCE = 'metadata/file/profile/screen-capture-api::capture-screen'
CASES = [
    ('capture', 'robotgo.CaptureScreen()', True),
    ('save', 'robotgo.SaveCapture(image, "capture.png")', False),
]
with tempfile.TemporaryDirectory(prefix='robotgo-capture-boundary-') as directory:
    for name, command, expected in CASES:
        target = Path(directory) / (name + '.go')
        target.write_text('package main\nfunc main() { ' + command + ' }\n' + '// padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', CAPTURE + ',' + REFERENCE], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule, match in ((CAPTURE, expected), (REFERENCE, True)):
            prefix = ('MATCHED ' if match else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
