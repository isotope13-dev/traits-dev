#!/usr/bin/env python3
"""Scan inert fixtures; never execute their source."""
import argparse
import json
import os
import io
import tarfile
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
fixture_dir = Path(__file__).resolve().parent
root = fixture_dir.parents[2]
cases = json.loads((fixture_dir / 'cases.json').read_text())
args.scratch.mkdir(parents=True, exist_ok=True)
for case in cases:
    (args.scratch / case['file']).write_bytes((fixture_dir / case.get('source', case['file'])).read_bytes())
archive_name = 'separate-hook-actions.tgz'
archive_path = args.scratch / archive_name
members = {
    'package/package.json': json.dumps({'name': 'setup-console', 'version': '1.0.0',
        'scripts': {'postinstall': 'node scripts/postinstall.js'}}).encode(),
    'package/scripts/postinstall.js': b'console.log("Run setup when needed");',
    'package/setup.js': b'const fs=require("fs"); const cp=require("child_process"); function setup(){cp.execSync("git rev-parse --git-dir"); fs.writeFileSync(".git/hooks/pre-commit", "#!/bin/sh\\necho check\\n", {mode:0o755}); fs.chmodSync(".git/hooks/pre-commit",0o755);} module.exports={setup};',
}
with tarfile.open(archive_path, 'w:gz') as archive:
    for name, data in members.items():
        info = tarfile.TarInfo(name)
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))
cases.append({'file': archive_name, 'no_hostile': True,
    'absent': ['objectives/persistence/system/git-hooks::postinstall-git-hook-install']})
result = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'jsonl',
     *[str(args.scratch / case['file']) for case in cases]],
    capture_output=True, text=True,
    env={**os.environ, 'RAYON_NUM_THREADS': '2'})
if result.returncode:
    raise SystemExit(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    report = json.loads(line)
    files = report['files']
    reports[Path(files[0]['path']).name] = files
for case in cases:
    files = reports[case['file']]
    findings = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
    for trait in case.get('present', []):
        assert trait in findings, (case['file'], 'missing', trait)
    for trait in case.get('absent', []):
        assert trait not in findings, (case['file'], 'unexpected', trait)
    if case.get('no_hostile'):
        assert not any(crit >= 5 for crit in findings.values()), case['file']
print(f"PASS: {len(cases)} registry-review controls")
