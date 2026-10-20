#!/usr/bin/env python3
"""Check the moved path observation and preservation of its direct consumer."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--work-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
key = r'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl'
cases = {
    'path.ps1': ("$key = '" + key + "'\n", True, False),
    'near-miss.ps1': ("$key = '" + key + "Other'\n", False, False),
    'hibernate.ps1': (
        "Set-ItemProperty -Path '" + key + "' -Name 'DumpFilters' -Value @()\n"
        "shutdown.exe /h\n", True, True),
}
path_id = 'micro-behaviors/os/registry/keys/policy::crash-control-registry-path'
old_id = 'micro-behaviors/os/registry/write::crash-control-registry-path'
consumer = 'objectives/impact/degrade/crypto::dump-filter-removal-before-hibernation'
args.work_dir.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='crashcontrol-controls-', dir=args.work_dir) as temp:
    for name, (content, _, _) in cases.items():
        (Path(temp) / name).write_text(content)
    result = subprocess.run([
        args.cleave, '--traits-dir', str(root), '--all-files', '--format', 'json', temp
    ], check=True, capture_output=True, text=True)
    assert not result.stderr.strip(), result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout
    seen = set()
    while remaining.strip():
        remaining = remaining.lstrip()
        report, length = decoder.raw_decode(remaining)
        remaining = remaining[length:]
        for file in report['files']:
            name = Path(file['path']).name
            ids = {t['id'] for t in file.get('traits', [])}
            assert old_id not in ids
            assert (path_id in ids) == cases[name][1], (name, ids)
            assert (consumer in ids) == cases[name][2], (name, ids)
            seen.add(name)
            print(name + ': PASS')
    assert seen == cases.keys()
print('3 controls passed')
