#!/usr/bin/env python3
"""Inert controls for Base64-repair placement and SuperH RC4 coverage."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
NEW = 'objectives/anti-static/obfuscation/encoding/base64::ps-regex-repaired-base64'
OLD = 'objectives/command-and-control/dropper/file-exec/command/batch::ps-regex-repaired-base64'
RC4 = 'micro-behaviors/crypto/symmetric/stream/rc4::superh-rc4-unrolled-buffer-transform'
spec = importlib.util.spec_from_file_location('fixtures', ROOT / 'testdata/taxonomy/mirai-native-review/check.py')
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
CODE = bytes.fromhex('30 60 0C 69 43 60 9C 38 8C 65 5C 01 10 23 94 05 30 61 B0 62 1C 39 9C 60 4C 01 1A 22 20 2B 70 60 0C 68 43 60 8C 35 5C 63 3C 01 10 27 84 03 70 61 C0 62 1C 38 8C 60 4C 01 1A 22 20 2C')
repair = b'$x=[Convert]::FromBase64String([regex]::Replace($s,"!","A"))\n'
cases = {
    'repair.ps1': (repair, {NEW}, {OLD}),
    'repair.cmd': (b'powershell -Command "' + repair + b'"', {NEW}, {OLD}),
    'ordinary.ps1': (b'$x=[Convert]::FromBase64String($s)\n', set(), {NEW, OLD}),
    'unrelated.ps1': (b'$x=[regex]::Replace($s,"a","b")\n', set(), {NEW, OLD}),
    'rc4.elf': (fixtures.elf(code=CODE, machine=42), {RC4}, set()),
    'no-xor.elf': (fixtures.elf(code=CODE.replace(bytes.fromhex('1A 22'), bytes.fromhex('19 22')), machine=42), set(), {RC4}),
    'wrong-section.elf': (fixtures.elf(rodata=CODE, machine=42), set(), {RC4}),
    'wrong-arch.elf': (fixtures.elf(code=CODE, machine=40), set(), {RC4}),
}
with tempfile.TemporaryDirectory(prefix='controls-', dir=Path(__file__).parent) as temp:
    paths = []
    for name, (data, _, _) in cases.items():
        path = Path(temp) / name
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run(['cleave', '--no-update-check', '--traits-dir', str(ROOT), '--disable', 'radare2,upx,third-party', '--format', 'json', *paths], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    reports = {Path(f['path']).name: f for f in fixtures.reports(result.stdout) if '##' not in f['path']}
    for name, (_, yes, no) in cases.items():
        ids = {t['id'] for t in reports[name]['traits']}
        assert yes <= ids and not no & ids, (name, yes - ids, no & ids)
        print('PASS', name)
