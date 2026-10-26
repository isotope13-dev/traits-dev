"""Static controls. Scan fixtures only; never run their commands or hooks."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EXPLOIT = 'objectives/lateral-movement/exploit/scanner::ci-random-target-cve-exploitation'
UPLOAD = 'objectives/exfiltration/stealer/credential::ci-credential-result-loop-http-upload'
BEACON = 'objectives/command-and-control/beacon/loop::ci-random-exploit-periodic-log-report'
CHUNK = 'micro-behaviors/communications/http/curl::shell-file-chunk-urlencoded-body'

parser = argparse.ArgumentParser()
parser.add_argument('--work-dir', required=True, type=Path)
args = parser.parse_args()
args.work_dir.mkdir(parents=True, exist_ok=True)
workflow = yaml.safe_load((HERE / 'runner.yml').read_text())
run = workflow['jobs']['run']['steps'][1]['run']
collect = workflow['jobs']['run']['steps'][2]['run']
variants = {
    'exploit.sh': run,
    'collect.sh': collect,
    'renamed.sh': run.replace('CHUNK', 'PART').replace('SRC', 'INPUT')
        .replace('/tmp/.svc', '/tmp/.worker').replace('43.228.157.68', '8.8.4.4')
        .replace('CVE-2026-41940', 'CVE-2025-12345'),
    'unlinked-body.sh': run.replace('content=$CHUNK', 'content=$UNRELATED'),
    'no-read.sh': re.sub(r'CHUNK=\$\(tail[^\n]+?\);', 'CHUNK="ready";', run),
    'ordinary-ci.sh': re.sub(r'\b[a-z][a-z0-9_]*_(creds|tokens)\.txt\b', 'results.txt', run)
        .replace('--source random', '--source file')
        .replace('--exploit CVE-2026-41940', '--check'),
    'fixed-target.sh': run.replace('--source random', '--source file'),
    'commented-exploit.sh': '# --source random --exploit CVE-2026-41940\n' + run.replace('--source random', '--source file'),
    'no-cve-exploit.sh': run.replace('--exploit CVE-2026-41940', '--check'),
    'no-log-field.sh': run.replace('log=$LINE', 'message=$LINE'),
}
for name, text in variants.items():
    (args.work_dir / name).write_text(text)
# These are inert inputs to the analyzer, including an honest installer and
# an encoded harmless program. They deliberately retain real capabilities.
(args.work_dir / 'setup.py').write_text('''from setuptools import setup
import os
os.system("curl -L https://vendor.example/source.tar.gz -o source.tar.gz")
setup(name="native-builder", version="1.0")
''')
(args.work_dir / 'package.json').write_text(json.dumps({
    'name': 'encoded-print', 'version': '1.0',
    'scripts': {'postinstall': 'node -e "eval(Buffer.from(\'Y29uc29sZS5sb2coMSk=\',\'base64\').toString())"'},
}))
(args.work_dir / 'uri-read.php').write_text("<?php eval(file_get_contents('php://input'));\n")
(args.work_dir / 'regex.go').write_text('package main\nimport "regexp"\nvar r = regexp.MustCompile(`\\bTRAVIS\\b`)\n')
targets = list(sorted(args.work_dir.glob('*.sh'))) + [
    args.work_dir / n for n in ['setup.py', 'package.json', 'uri-read.php', 'regex.go']
] + [HERE / 'tasks.json']
completed = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--json', *map(str, targets)],
                           text=True, capture_output=True, check=True)
(args.work_dir / 'controls.jsonl').write_text(completed.stdout)
(args.work_dir / 'controls.log').write_text(completed.stderr)
reports = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
by_name = {}
for report in reports:
    for f in report['files']:
        if f['id'] == 0:
            by_name[Path(f['path']).name] = {t['id']: t['crit'] for t in f.get('traits', [])}
checks = 0

def expect(name, present=(), absent=()):
    global checks
    traits = by_name[name]
    for trait in present:
        assert trait in traits, (name, 'missing', trait)
        checks += 1
    for trait in absent:
        assert trait not in traits, (name, 'unexpected', trait)
        checks += 1

for name in ['exploit.sh', 'renamed.sh']:
    expect(name, [EXPLOIT, UPLOAD, BEACON, CHUNK])
expect('collect.sh', [UPLOAD, CHUNK], [EXPLOIT, BEACON])
expect('unlinked-body.sh', [EXPLOIT, BEACON], [UPLOAD, CHUNK])
expect('no-read.sh', [EXPLOIT, BEACON], [UPLOAD, CHUNK])
expect('ordinary-ci.sh', [CHUNK], [EXPLOIT, UPLOAD, BEACON])
expect('fixed-target.sh', [UPLOAD], [EXPLOIT, BEACON])
expect('commented-exploit.sh', [UPLOAD], [EXPLOIT, BEACON])
expect('no-cve-exploit.sh', [UPLOAD], [EXPLOIT, BEACON])
expect('no-log-field.sh', [EXPLOIT, UPLOAD], [BEACON])
for name in ['setup.py', 'package.json', 'tasks.json', 'uri-read.php', 'regex.go']:
    assert not any(c >= 4 for c in by_name[name].values()), (name, by_name[name])
    checks += 1
expect('tasks.json', ['metadata/package/scripts/command::vscode-task-windows-command',
                     'metadata/permission/activation::vscode-task-folder-open-activation'])
expect('package.json', ['micro-behaviors/process/create/eval::manifest-inline-conversion-no-repository'])
expect('uri-read.php', ['micro-behaviors/process/deploy/script-eval::php-eval-uri-read-text'],
       ['micro-behaviors/process/deploy/script-eval::php-eval-http-read-text'])
expect('regex.go', ['metadata/lang/source/naming/target::vm-ci-word-boundary-regex'])
print(f'{checks} assertions passed across {len(by_name)} static controls')
