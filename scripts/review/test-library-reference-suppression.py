#!/usr/bin/env python3
"""A library name must not suppress an XZ-style linker indicator."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
CLANG = os.environ.get('CLANG', 'clang')
INDICATOR = 'micro-behaviors/os/linker::rtld-global-ref'
LIBRARY = 'micro-behaviors/communications/http/client/reference::libcurl-ref'
with tempfile.TemporaryDirectory(prefix='library-reference-') as directory:
    source = Path(directory) / 'fixture.c'
    target = Path(directory) / 'fixture.o'
    source.write_text('const char fixture[] = "__rtld_global libcurl";\n')
    subprocess.run([CLANG, '-target', 'x86_64-unknown-linux-gnu', '-c', str(source), '-o', str(target)], check=True)
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                             '--rules', INDICATOR + ',' + LIBRARY], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    for rule in (INDICATOR, LIBRARY):
        assert any(line.startswith('MATCHED ' + rule + ' ') for line in result.stdout.splitlines()), result.stdout
    print('library name does not suppress linker indicator: passed', flush=True)
