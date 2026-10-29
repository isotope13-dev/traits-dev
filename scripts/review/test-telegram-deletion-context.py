#!/usr/bin/env python3
"""Deletion context requires a bound call or a child-code binding."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULES = ('micro-behaviors/communications/messaging/telegram::goygram-account-delete-request',
         'micro-behaviors/communications/messaging/telegram::goygram-detached-delete-template',
         'objectives/impact/destroy/messaging::detached-telegram-delete-template')


def source(bound):
    code = '''from goygram import security
await client.send({{'_':'account.deleteAccount','reason':''}})'''
    child = 'code' if bound else 'other'
    return f'''import subprocess, sys
from goygram import security
def run():
    code = """{code}"""
    subprocess.Popen([sys.executable, '-c', {child}], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
''' + '\n#' + ' padding' * 90 + '\n'


with tempfile.TemporaryDirectory(prefix='telegram-deletion-probe-') as directory:
    for name, expected in [('bound', True), ('unbound', False)]:
        target = Path(directory) / (name + '.py')
        target.write_text(source(expected))
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                                 str(target), '--rules', ','.join(RULES)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule in RULES:
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, rule, result.stdout)
        print(name + ': passed', flush=True)
