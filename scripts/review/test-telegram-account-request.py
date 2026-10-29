#!/usr/bin/env python3
"""Deletion evidence must be a request call or code bound to a child sink."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULES = ('micro-behaviors/communications/messaging/telegram::account-delete-request-call',
         'micro-behaviors/communications/messaging/telegram::account-delete-template-child')
CASES = (
    ('direct', '''async def run(client):
    await client.send({'_': 'account.deleteAccount', 'reason': ''})
''', (True, False)),
    ('template', '''import subprocess, sys
def run():
    code = """await client.send({{'_':'account.deleteAccount','reason':''}})"""
    subprocess.Popen([sys.executable, '-c', code])
''', (False, True)),
    ('unbound', '''import subprocess, sys
def run():
    code = """await client.send({{'_':'account.deleteAccount','reason':''}})"""
    subprocess.Popen([sys.executable, '-c', other])
''', (False, False)),
    ('reference', '''description = "account.deleteAccount"
''', (False, False)),
)

with tempfile.TemporaryDirectory(prefix='telegram-account-probe-') as directory:
    for name, source, expected in CASES:
        target = Path(directory) / (name + '.py')
        target.write_text(source + '\n#' + ' padding' * 90 + '\n')
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                                 str(target), '--rules', ','.join(RULES)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule, matches in zip(RULES, expected):
            prefix = ('MATCHED ' if matches else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, rule, result.stdout)
        print(name + ': passed', flush=True)
