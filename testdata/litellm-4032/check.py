#!/usr/bin/env python3
"""Focused assertions for article 4032; controls live in cleave's fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--fixtures', type=Path, required=True)
parser.add_argument('--report', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                'analyze', str(args.fixtures), '-o', str(args.report)], check=True)
s = args.report.read_text()
dec = json.JSONDecoder()
files = {}
while s.strip():
    d, n = dec.raw_decode(s.lstrip())
    s = s.lstrip()[n:]
    for f in d.get('files', []):
        files[str(Path(f['path']).relative_to(args.fixtures))] = {
            t['id']: t['crit'] for t in f.get('traits', [])}

sql = {'micro-behaviors/data/db/query::litellm-credential-values-query',
       'micro-behaviors/data/db/query::litellm-model-params-query'}
dump = 'objectives/credential-access/dev-tools/ai::litellm-provider-database-dump'
export = 'objectives/exfiltration/stealer/dev-secret::litellm-provider-database-http-export'
poll = 'objectives/command-and-control/remote-command/http-poll::python-helper-response-exec-poll'
daemon = 'objectives/command-and-control/remote-command/http-poll::python-detached-helper-exec-poll'
startup = 'objectives/persistence/system/python-startup::startup-hook-helper-code-daemon'
checks = 0

def expect(name, required=(), forbidden=()):
    global checks
    found = files[name]
    missing = set(required) - found.keys()
    extra = set(forbidden) & found.keys()
    assert not missing and not extra, (name, sorted(missing), sorted(extra))
    checks += 1

for name in ('collector.py', 'httpx_collector.py', 'collector.js', 'collector.ts', 'cook.py'):
    expect('positive/' + name, sql | {dump, export})
expect('positive/sitecustomize.py', {poll, daemon, startup})
expect('positive/renamed_loader.py', {poll, daemon}, {startup})
for name in ('backup.py', 'overwritten.py', 'overwritten.js', 'unrelated_post.py',
             'star_backup.py', 'backup.go', 'backup.rb', 'Backup.java', 'backup.php'):
    expect('benign/' + name, sql | {dump}, {export, poll, daemon, startup})
for name in ('counts.py', 'column_counts.py', 'names_only.py', 'comment_only.py',
             'table_prefix.py', 'query_prose.py', 'sitecustomize.py',
             'overwritten_loader.py', 'unrelated_loader.py'):
    expect('benign/' + name, forbidden=sql | {dump, export, poll, daemon, startup})
expect('benign/dynamic_base64.py', {'metadata/import/package::python-dunder-base64-import', 'micro-behaviors/os/module/load::dunder-import-call'})
expect('benign/quoted_base64.py', forbidden={'metadata/import/package::python-dunder-base64-import', 'micro-behaviors/os/module/load::dunder-import-call'})
expect('benign/dynamic_zlib.py', {'metadata/import/package::python-dynamic-zlib-import', 'micro-behaviors/os/module/load::dunder-import-call'})
expect('benign/quoted_zlib.py', forbidden={'metadata/import/package::python-dynamic-zlib-import', 'micro-behaviors/os/module/load::dunder-import-call'})
print(f'{checks} focused fixture cases passed')
