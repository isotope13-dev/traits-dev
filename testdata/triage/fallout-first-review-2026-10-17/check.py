"""Static regression controls; usage: check.py ZOMBIE_SAMPLE SCRATCH.

Specimen mutations test evidence dependencies, not benignness of altered malware.
The RET-entry reference-table control is inert. Nothing here executes a specimen.
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FILTER = 'micro-behaviors/fs/search::x86-four-suffix-shared-action'
DELETE = 'objectives/impact/destroy/file-deletion::drive-backup-suffix-deletion'
INFECT = 'objectives/impact/infect/binary/rewrite::packed-drive-executable-joiner'
FAMILY = 'well-known/malware/virus/zombie::zombie-packed-file-infector'
TARGETS = {FILTER, DELETE, INFECT, FAMILY}


def main():
    specimen = Path(sys.argv[1]).read_bytes()
    scratch = Path(sys.argv[2])
    scratch.mkdir(parents=True, exist_ok=True)
    start = bytes.fromhex('8b 54 24 24 68 08 41 40 00 52 ff d5')
    branch = specimen.index(start)
    broken = bytearray(specimen)
    assert broken[branch + 17] == 0x74
    broken[branch + 17] = 0x75
    relocated = bytearray(specimen)
    # Rebase the four immediate operands, leaving opcodes and branches intact.
    # This is a matcher-generalization control, not a runnable rebuilt image.
    for pos in (5, 24, 43, 62):
        relocated[branch + pos:branch + pos + 4] = b'\x10\x22\x60\x00'
    no_identity = specimen.replace(b'\\Zombie.exe', b'\\Helper.exe').replace(
        bytes.fromhex('cf eb d5 d2 bb d8 ce c4 bc fe 2d 5f 2d'), b'x' * 13)
    image = runpy.run_path(str(ROOT / 'testdata/triage-sighted/build_pe_fixtures.py'))['image']
    table = (b'.BAK\0\0\0\0.bak\0\0\0\0.GHO\0\0\0\0gho\0.EXE\0'
             b'\0fopen\0\0rename\0\0fwrite\0DeleteFileA\0GetLogicalDrives\0'
             b'UPX!\0\\Zombie.exe\0' +
             bytes.fromhex('cf eb d5 d2 bb d8 ce c4 bc fe 2d 5f 2d'))
    cases = {
        'original.exe': (specimen, TARGETS),
        'rebased-operands.exe': (bytes(relocated), TARGETS),
        'changed-branch.exe': (bytes(broken), set()),
        'without-backup-table.exe': (
            specimen.replace(b'.GHO\0', b'.LOG\0'), {FILTER}),
        'without-delete-api.exe': (
            specimen.replace(b'DeleteFileA\0', b'UpdateFileA\0'), {FILTER}),
        'without-family-labels.exe': (no_identity, {FILTER, DELETE, INFECT}),
        'reference-table-only.exe': (image(b'.data', table, 16384), set()),
    }
    paths = []
    for name, (content, _) in cases.items():
        path = scratch / name
        path.write_bytes(content)
        paths.append(str(path))
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', *paths,
    ], capture_output=True, text=True, check=True)
    (scratch / 'reports.jsonl').write_text(result.stdout)
    (scratch / 'stderr.txt').write_text(result.stderr)
    decoder, pending, observed = json.JSONDecoder(), result.stdout.strip(), {}
    while pending:
        report, end = decoder.raw_decode(pending)
        for file in report['files']:
            observed[Path(file['path']).name] = {
                trait['id'] for trait in file.get('traits', [])}
        pending = pending[end:].strip()
    for name, (_, expected) in cases.items():
        actual = observed[name] & TARGETS
        assert actual == expected, (name, actual, expected)
    print(json.dumps({'cases': len(cases), 'failures': []}, indent=2))


if __name__ == '__main__':
    main()
