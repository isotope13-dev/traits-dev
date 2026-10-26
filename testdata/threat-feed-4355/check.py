#!/usr/bin/env python3
"""Check HTTP handshake routes without executing any fixture code."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--fixtures', type=Path, required=True)
parser.add_argument('--report', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
args.fixtures.mkdir(parents=True, exist_ok=True)
route = 'micro-behaviors/communications/http/url/api-path::upload-handshake-route'
family = 'well-known/malware/stealer/aokigahara::chunked-upload-protocol'
cases = {
    'bare.py': ('route = "/handshake"\n', True, False),
    'prefixed.py': ('route = "/gate/handshake"\n', True, False),
    'query.js': ('const route = "https://rotated.invalid/v3/gate/handshake?sid=x";\n', True, False),
    'filename.py': ('module = "../lib/handshake.ts"\n', False, False),
    'helper.py': ('module = "/gate/handshake_helper.py"\n', False, False),
    'prefix.py': ('route = "/gate/handshakes"\n', False, False),
    'family.js': ('const endpoints = ["/gate/handshake", "/gate/chunk", "/gate/complete"]; const header = "X-Gate-Token";\n', True, True),
    'generic-upload.js': ('const endpoints = ["/gate/handshake", "/gate/chunk", "/gate/complete"]; const header = "Authorization";\n', True, False),
    'native.c': ('const char *routes[] = {"/gate/handshake", "/gate/chunk", "/gate/complete", "X-Gate-Token"}; int probe(void) { return routes[0][0]; }\n', True, True),
}
for name, (source, _, _) in cases.items():
    (args.fixtures / name).write_text(source)
native = 'native.dylib' if sys.platform == 'darwin' else 'native.so'
subprocess.run(['cc', '-shared', '-o', str(args.fixtures / native),
                str(args.fixtures / 'native.c')], check=True)
expected = {name: (r, f) for name, (_, r, f) in cases.items()}
expected[native] = (True, True)
root = Path(__file__).resolve().parents[2]
subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                str(args.fixtures), '-o', str(args.report)], check=True)
text = args.report.read_text()
seen = set()
while text.strip():
    report, end = json.JSONDecoder().raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for file in report['files']:
        name = Path(file['path']).name
        if name not in expected:
            continue
        ids = {trait['id'] for trait in file.get('traits', [])}
        actual = (route in ids, family in ids)
        assert actual == expected[name], (name, actual, expected[name])
        seen.add(name)
assert seen == set(expected), sorted(set(expected) - seen)
print(f'{len(seen)} route and family controls passed')
