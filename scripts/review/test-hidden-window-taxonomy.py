#!/usr/bin/env python3
"""Verify hidden-window evidence is specific and not suppressed by path/tool context."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='hidden-window-taxonomy-') as tmp:
    root = Path(tmp)
    (root / 'testdata').mkdir()
    hidden = 'powershell -w hidden -c Write-Output hello\nrem AppDeployToolkit\n'
    cases = {
        'plain.bat': 'powershell -nop -c Write-Output hello\n',
        'word.bat': 'powershell -w Hello -c Write-Output hello\n',
        'hidden.bat': hidden,
        'testdata/hidden.bat': hidden,
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(root / name) for name in cases)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {str(Path(r['path']).relative_to(root)): {t['id']: t for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    command = 'metadata/lang/source/syntax/command/launch::batch-powershell-noprofile-command'
    hidden_trait = 'micro-behaviors/process/argument/visibility::powershell-hidden-window'
    assert command in ids['plain.bat'] and hidden_trait not in ids['plain.bat']
    assert hidden_trait not in ids['word.bat']
    for name in ('hidden.bat', 'testdata/hidden.bat'):
        assert hidden_trait in ids[name] and ids[name][hidden_trait]['crit'] == 3, (name, ids[name].get(hidden_trait))
    print('Hidden-window text requires the option and survives path/tool context.')

    fixtures = [
        'testdata/suspicious/generated/stranded-empire-davtest-mettle/controls/different-registry-key.ps1',
        'testdata/notable/generated/stranded-empire-davtest-mettle/controls/documented-pipeline.ps1',
        'testdata/suspicious/generated/taxonomy/concealed-task-resource-review/socket-without-eval.ps1',
    ]
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(repo / name) for name in fixtures)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    by_name = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    profile = 'metadata/file/profile/registry/access::hidden-encoded-silentcleanup-property-clues'
    task = 'objectives/persistence/login/scheduled-task/interval::short-interval-hidden-encoded-system-task'
    assert profile in by_name['different-registry-key.ps1']
    assert profile not in by_name['documented-pipeline.ps1']
    assert task in by_name['socket-without-eval.ps1']
    print('Suspicious combinations match independently of comment-only text.')
