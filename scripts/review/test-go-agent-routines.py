#!/usr/bin/env python3
"""Require each behavioral routine name in a compiled Go binary."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/command-and-control/backdoor/agent::go-agent-injection-persistence-c2'
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    (d / 'go.mod').write_text('module example.invalid/review\n\ngo 1.20\n')
    agent = d / 'internal' / 'agent'
    agent.mkdir(parents=True)
    (agent / 'agent.go').write_text('''package agent
var sink int
//go:noinline
func InjectShellcode() { sink++ }
//go:noinline
func PersistAllInOne() { sink++ }
//go:noinline
func ConnectCC() { sink++ }
//go:noinline
func reverseShell() { sink++ }
func Launch() { InjectShellcode(); PersistAllInOne(); ConnectCC(); reverseShell() }
''')
    (d / 'main.go').write_text('package main\nimport "example.invalid/review/internal/agent"\nfunc main(){ agent.Launch() }\n')
    base = d / 'full'
    subprocess.run(['go', 'build', '-buildvcs=false', '-trimpath', '-o', str(base), '.'], cwd=d, check=True,
                   env={**os.environ, 'CGO_ENABLED':'0', 'GOPROXY':'off'})
    payload = base.read_bytes()
    variants = [('full', payload, True)]
    for token in (b'InjectShellcode', b'PersistAllInOne', b'ConnectCC', b'reverseShell'):
        assert b'/internal/agent.' + token in payload
        variants.append(('missing_' + token.decode(), payload.replace(b'/internal/agent.' + token, b'/internal/agent.' + b'X' * len(token)), False))
    for name, data, expected in variants:
        path = d / name
        path.write_bytes(data)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                                check=True, capture_output=True, text=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE':'1'})
        found = any(t['id'] == RULE for f in json.loads(result.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('Compiled Go agent routine boundaries passed')
