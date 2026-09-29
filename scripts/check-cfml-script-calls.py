#!/usr/bin/env python3
"""Test CFScript credential evidence independently of genuine shell behavior."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
fixtures = r / 'testdata/taxonomy/cfml-script-calls'
assert hashlib.sha256((fixtures / 'retained-original.cfm').read_bytes()).hexdigest() == '987de3c74aaa5371c98365b281fdc3c4b680558aae5b4c9895ec6b8c9fc083d2'
java = 'micro-behaviors/process/interpreter/runtime/jvm::cfml-java-createobject'
factory = 'micro-behaviors/process/interpreter/runtime/jvm::cfml-service-factory-createobject'
enum = 'micro-behaviors/data/db/config::cfml-datasource-service-enumeration'
decrypt = 'micro-behaviors/crypto/symmetric/decrypt::cfml-decrypt-password-member'
objective = 'objectives/credential-access/theft/app::cfml-webshell-datasource-password-decryption'
selected = {java, factory, enum, decrypt, objective}
expected = {name: selected for name in ('direct', 'inline-comments', 'retained-original')}
expected.update({name: set() for name in ('commented', 'quoted', 'java-argument-reversed')})
expected.update({name: {java, factory, enum} for name in ('commented-decrypt', 'wrong-password-argument', 'wrong-password-member', 'quoted-password-member')})
expected['no-command'] = {java, factory, enum, decrypt}
paths = sorted(fixtures.glob('*.cfm'))
assert {path.stem for path in paths} == set(expected)
for path in paths:
    result = subprocess.run([a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    assert ids & selected == expected[path.stem], (path.name, traits)
    shell = 'objectives/command-and-control/backdoor/webshell/request::cfml-request-command-shell'
    if path.stem in {'no-command', 'java-argument-reversed'}:
        assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    else:
        assert shell in ids, (path.name, traits)
    assert 'micro-behaviors/data/db/config::cfml-service-factory-class' not in ids
    assert 'micro-behaviors/crypto/symmetric/decrypt::cfml-decrypt-indexed-password' not in ids
    print(path.stem + ': passed', flush=True)
