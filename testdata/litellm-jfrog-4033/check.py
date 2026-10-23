#!/usr/bin/env python3
"""Verify query and helper-flow boundaries with cleave-owned fixtures."""
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

sql_prefix = 'micro-behaviors/data/db/query::'
direct = {sql_prefix + 'litellm-' + part + '-bulk-query'
          for part in ('credentials', 'models')}
forwarded = {sql_prefix + 'python-forwarded-litellm-' + part + '-query'
             for part in ('credentials', 'models')}
php = {sql_prefix + 'php-litellm-' + part + '-query'
       for part in ('credentials', 'models')}
http = 'micro-behaviors/process/deploy/script-eval::python-http-helper-compiled-exec'
startup = 'objectives/persistence/system/python-startup::startup-hook-http-helper-daemon'
checks = 0


def expect(name, required=(), forbidden=()):
    global checks
    found = files[name]
    missing = set(required) - found.keys()
    extra = set(forbidden) & found.keys()
    assert not missing and not extra, (name, sorted(missing), sorted(extra))
    for trait in (direct | forwarded | php | {http}) & found.keys():
        assert found[trait] in (3, 'notable'), (name, trait, found[trait])
    checks += 1


for suffix in ('py', 'js', 'ts', 'rb', 'go', 'java'):
    expect('backup.' + suffix, direct, {http, startup})
expect('backup.php', php, {http, startup})
expect('star.py', direct, {http, startup})
for name in ('count.py', 'prefix.py', 'other_table.py', 'query_prose.py', 'log_sql.py',
             'comments.py', 'quoted.py', 'php_prose.php', 'php_count.php',
             'php_prefix.php', 'php_logger.php'):
    expect(name, forbidden=direct | forwarded | php | {http, startup})
for name in ('positive/sitecustomize.py', 'positive/usercustomize.py'):
    expect(name, forwarded | {http, startup})
expect('plugin.py', forwarded | {http}, {startup})
expect('helper_renamed.py', forwarded | {http}, {startup})
for name in ('overwritten.py', 'different_value.py', 'different_helper.py',
             'not_http.py', 'compile_only.py', 'wrong_mode.py',
             'negative/sitecustomize.py'):
    expect(name, forwarded, {http, startup})
for name in ('db_wrong_parameter.py', 'db_wrong_helper.py',
             'db_other_tables.py', 'db_comment.py'):
    expect(name, {http}, forwarded | {startup})
expect('plain.py##plain@0x10', forbidden=forwarded | {http, startup})
old = 'objectives/command-and-control/remote-command/http-poll::python-polled-response-compiled-executor'
expect('old_compiled_daemon.py', {old}, {http, startup})
expect('old_compiled.py##plain@0x20', forbidden=forwarded | {http, startup, old})
export = 'objectives/exfiltration/stealer/dev-secret::python-source-control-credential-post'
retired = 'objectives/credential-access/files/config::python-github-credential-file-harvest'
expect('git_export.py', {export}, {retired})
expect('git_read_only.py', forbidden={export, retired})
assert all(retired not in found for found in files.values())
codecs = {'metadata/import/package::python-dunder-base64-import',
          'micro-behaviors/os/module/load::python-dynamic-zlib-import',
          'micro-behaviors/os/module/load::python-dynamic-codec-imports'}
expect('dynamic_codecs.py', codecs)
for name in ('codec_comment.py', 'codec_literal.py', 'wrong_codecs.py'):
    expect(name, forbidden=codecs)
print(f'{checks} focused cases passed')
