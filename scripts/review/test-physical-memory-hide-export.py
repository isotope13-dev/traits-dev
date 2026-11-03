#!/usr/bin/env python3
"""Exercise PE export, physical-device, and mapping evidence independently."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/evasion/kernel-hide/rootkit::process-hide-physical-memory'
BASE = r'''
__declspec(dllimport) void *MAP_FUNCTION(void);
__declspec(dllexport) const unsigned short physical[] = {DEVICE_CHARS};
__declspec(dllexport) const char section[] = "SECTION_NAME";
__declspec(dllexport) int EXPORT_NAME(void) { return MAP_FUNCTION() != 0; }
'''
cases = [
    ('all', 'HideProcess', 'PhysicalMemory', 'ZwOpenSection', 'MapViewOfFile', True),
    ('other_export', 'ShowProcess', 'PhysicalMemory', 'ZwOpenSection', 'MapViewOfFile', False),
    ('other_device', 'HideProcess', 'VirtualMemory', 'ZwOpenSection', 'MapViewOfFile', False),
    ('other_section', 'HideProcess', 'PhysicalMemory', 'ZwQuerySection', 'MapViewOfFile', False),
    ('other_import', 'HideProcess', 'PhysicalMemory', 'ZwOpenSection', 'ReadFile', False),
]
with tempfile.TemporaryDirectory() as tmp:
    directory = Path(tmp)
    for name, export, device, section, mapped, expected in cases:
        stem = directory / name
        source = BASE.replace('MAP_FUNCTION', mapped).replace('EXPORT_NAME', export).replace('SECTION_NAME', section)
        chars = ','.join(str(ord(c)) for c in '\\Device\\' + device) + ',0'
        source = source.replace('DEVICE_CHARS', chars)
        stem.with_suffix('.c').write_text(source)
        stem.with_suffix('.def').write_text('LIBRARY KERNEL32.dll\nEXPORTS\n' + mapped + '\n')
        subprocess.run(['llvm-dlltool', '-m', 'i386:x86-64', '-d', str(stem.with_suffix('.def')), '-l', str(stem.with_suffix('.lib'))], check=True, capture_output=True)
        subprocess.run(['clang', '--target=x86_64-pc-windows-msvc', '-c', str(stem.with_suffix('.c')), '-o', str(stem.with_suffix('.obj'))], check=True, capture_output=True)
        subprocess.run(['lld-link', '/dll', '/noentry', '/nodefaultlib', '/out:' + str(stem.with_suffix('.dll')), str(stem.with_suffix('.obj')), str(stem.with_suffix('.lib'))], check=True, capture_output=True)
        proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(stem.with_suffix('.dll'))],
                              check=True, capture_output=True, text=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        found = any(t['id'] == RULE for f in json.loads(proc.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('Physical-memory process-hiding evidence boundaries passed')
