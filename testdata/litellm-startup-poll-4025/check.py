#!/usr/bin/env python3
"""Check focused traits against controls kept in cleave's fixture tree."""
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
text = args.report.read_text()
decoder = json.JSONDecoder()
files = {}
while text.strip():
    value, end = decoder.raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for item in value['files']:
        name = str(Path(item['path']).relative_to(args.fixtures))
        files[name] = {trait['id']: trait['crit'] for trait in item.get('traits', [])}

sql = {'micro-behaviors/data/db/query::litellm-credential-values-query',
       'micro-behaviors/data/db/query::litellm-model-params-query'}
poll = 'objectives/command-and-control/remote-command/http-poll::python-http-response-exec-poll'
daemon = 'objectives/command-and-control/remote-command/http-poll::python-detached-http-exec-poll'
startup = 'objectives/persistence/login/python-startup::python-startup-http-exec-poll'
upload = 'objectives/exfiltration/stealer/credential::python-credential-http-upload'
old_upload = 'objectives/exfiltration/stealer/dev-secret::python-credential-http-upload'
checks = 0

def expect(name, required=(), forbidden=()):
    global checks
    found = files[name]
    missing = set(required) - found.keys()
    extra = set(forbidden) & found.keys()
    assert not missing and not extra, (name, sorted(missing), sorted(extra))
    assert old_upload not in found, name
    checks += 1

for name in ('agent.py', 'httpx_agent.py'):
    expect(name, sql | {poll, daemon}, {startup})
expect('positive/sitecustomize.py', sql | {poll, daemon, startup})
for name in ('backup.py', 'backup.js', 'backup.ts', 'backup.go', 'backup.rb', 'Backup.java'):
    expect(name, sql, {poll, daemon, startup, upload})
for name in ('overwritten.py', 'different_value.py'):
    expect(name, sql, {poll, daemon, startup})
for name in ('single_fetch.py', 'unrelated_loop.py', 'ordinary.py',
             'benign/sitecustomize.py', 'comment_only.py', 'count.py',
             'query_prose.py', 'other_table.py', 'table_prefix.py',
             'not_a_call.py', 'prose_only.py'):
    expect(name, forbidden=sql | {poll, daemon, startup})
print(f'{checks} focused fixture cases passed')
