#!/usr/bin/env python3
"""Check background-job placement and independent MSHTA command evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='background-job-') as tmp:
    root = Path(tmp)
    cases = {
        'job.ps1': 'Start-Job -ScriptBlock { Get-Date }\n',
        'comment.ps1': '# Start-Job -ScriptBlock { Get-Date }\n',
        'blank.ps1': 'mshta about:blank\n',
        'mixed.ps1': 'mshta about:<html>\n$x = "about:blank"\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    job = 'micro-behaviors/process/work/task::powershell-start-job-call'
    about = 'metadata/lang/source/syntax/command/launch::mshta-inline-about-document'
    assert job in ids['job.ps1'] and job not in ids['comment.ps1'], ids
    assert about in ids['blank.ps1'] and about in ids['mixed.ps1'], ids
    print('Background jobs and MSHTA about-command references remain distinct.')
