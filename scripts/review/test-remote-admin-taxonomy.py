#!/usr/bin/env python3
"""Check tool references and unbound remote-administration clues."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='remote-admin-taxonomy-') as tmp:
    root = Path(tmp)
    (root / 'testdata').mkdir()
    # Both names describe legitimate admin capabilities; none proves hostile intent.
    content = ('@echo off\nwmic /node:"%TARGET%" process call create calc.exe\n'
               'net use \\\\%TARGET%\\admin$\n'
               'psexec \\\\server cmd.exe\n'
               'wmiexec.py user@example.com\n')
    paths = [root / 'admin.bat', root / 'testdata' / 'admin.bat']
    for path in paths:
        path.write_text(content)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(path) for path in paths)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    by_path = {Path(report['path']): {t['id']: t for t in report.get('traits', [])} for report in reports}
    assert set(by_path) == set(paths), by_path.keys()
    expected = {
        'micro-behaviors/os/wmi/remote::batch-wmic-target-process-create',
        'micro-behaviors/network/share::batch-target-admin-share-path',
        'metadata/file/profile/co-occurrence/network-process::batch-wmic-admin-share-clues',
        'well-known/tool/sysadmin/sysinternals::psexec-remote-invocation',
        'well-known/tool/offensive/impacket::impacket-wmiexec-target',
    }
    for path in paths:
        missing = expected - set(by_path[path])
        assert not missing, (path, missing)
        for trait_id in expected:
            assert by_path[path][trait_id]['crit'] == 3, (path, trait_id, by_path[path][trait_id])
        assert 'objectives/execution/wmi/script::batch-panos-wmi-admin-remote-exec' not in by_path[path]
        print('PASS', path.relative_to(root))
