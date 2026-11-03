#!/usr/bin/env python3
"""Check DOS write-pattern evidence and neutral interrupt/file combinations."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
base = 'objectives/impact/infect/binary/dos/'
append_id = base + 'file::dos-searched-append-entry-patch'
header_id = base + 'file::dos-resident-exec-mz-header-patch'
generic_ids = {
    'micro-behaviors/fs/file/read-write::dos-search-write-time-sequences',
    'micro-behaviors/fs/file/read-write::dos-read-seek-write-time-sequences',
    'micro-behaviors/os/msdos/interrupt::dos-vector-and-file-service-sequences',
}
find_time = bytes.fromhex('B4 4E CD 21 B8 01 57 CD 21')
vectors = bytes.fromhex('B8 21 35 CD 21 B8 21 25 CD 21 3D 00 4B 74 01')
entry = bytes.fromhex('B9 03 00 B8 00 3F CD 21 B9 00 00 8B D1 B8 02 42 CD 21 8B D0 B9 58 02 B8 00 40 CD 21 72 27 B9 00 00 8B D1 B8 00 42 CD 21 BA 59 00 B9 03 00 B8 00 40 CD 21')
header = bytes.fromhex('B8 00 42 CD 21 B9 FB 03 BA 00 00 B8 00 40 CD 21 72 14 33 C9 8B D1 B8 00 42 CD 21 BA 03 01 B9 1C 00 B8 00 40 CD 21')
cases = {
    'entry.bin': (find_time + entry, {append_id}),
    'no-entry-write.bin': (find_time + entry.replace(bytes.fromhex('B9 03 00 B8 00 40'), bytes.fromhex('B9 04 00 B8 00 40')), set()),
    'no-search.bin': (entry, set()),
    'nonzero-seek.bin': (find_time + entry.replace(bytes.fromhex('B9 00 00 8B D1 B8 00 42'), bytes.fromhex('B9 01 00 8B D1 B8 00 42')), set()),
    'header.bin': (vectors + header, {header_id}),
    'no-vector.bin': (vectors.replace(bytes.fromhex('B8 21 25'), bytes.fromhex('B8 20 25')) + header, set()),
    'no-exec.bin': (vectors.replace(bytes.fromhex('3D 00 4B'), bytes.fromhex('3D 00 4A')) + header, set()),
    'wrong-header-length.bin': (vectors + header.replace(bytes.fromhex('B9 1C 00'), bytes.fromhex('B9 1B 00')), set()),
    'generic-calls.bin': (find_time + vectors + bytes.fromhex('B8 00 3F CD 21 B8 02 42 CD 21 B8 00 40 CD 21 B8 00 42 CD 21'), set()),
}
with tempfile.TemporaryDirectory(prefix='dos-entry-review-') as tmp:
    paths = []
    for name, (data, _) in cases.items():
        path = Path(tmp) / name
        path.write_bytes(data + b"\x90" * 256)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).name
        traits = {t['id']: t['crit'] for t in report.get('traits', [])}
        actual = {append_id, header_id} & traits.keys()
        assert actual == cases[name][1], (name, actual, cases[name][1])
        assert all(traits.get(key, 4) < 5 for key in generic_ids), (name, traits)
print('DOS entry and executable-header boundaries passed.')
