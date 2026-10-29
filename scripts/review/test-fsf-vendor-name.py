#!/usr/bin/env python3
"""Check the FSF binary-name observation against synthetic PE files.

Requires clang, lld-link and the sibling Cleave release binary. The files are
compiled for analysis only and are never executed.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
RULE = 'metadata/vendor/string::fsf-name-in-text-section'

with tempfile.TemporaryDirectory(prefix='fsf-vendor-name-') as temp:
    work = Path(temp)
    for case, value, section, expected in (
        ('name-only', 'Free Software Foundation, Inc.', '.text', True),
        ('different-name', 'Free Software Federation, Inc.', '.text', False),
        ('different-section', 'Free Software Foundation, Inc.', '.rdata', False),
    ):
        source, obj, executable = (work / (case + ext) for ext in ('.c', '.obj', '.exe'))
        source.write_text(f'__declspec(allocate("{section}")) volatile const char marker[] = '
                          f'"{value}";\nint main(void) {{ return marker[0]; }}\n')
        subprocess.run(['clang', '-target', 'x86_64-pc-windows-msvc', '-c', str(source),
                        '-o', str(obj)], check=True)
        subprocess.run(['lld-link', '/entry:main', '/subsystem:console', '/nodefaultlib',
                        '/out:' + str(executable), str(obj)], check=True)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', RULE, str(executable)], check=True,
                                capture_output=True, text=True)
        summary = f'Summary: {int(expected)} matched, {int(not expected)} not matched'
        if summary not in result.stdout:
            raise SystemExit(f'{case}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{case}: ok', flush=True)
