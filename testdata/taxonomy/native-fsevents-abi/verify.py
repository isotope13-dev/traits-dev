#!/usr/bin/env python3
"""Check native imports, literal/definition near misses, and retained attacks."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WATCH = 'micro-behaviors/fs/watch::fseventstream-create-import'
ABI = 'metadata/binary/symbols/abi-name::node-cpp-abi-import'
MISMATCH = 'metadata/file/extension/mismatch::node-addon-without-abi-references'
STARTUP = 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-startup-native-abi-mismatch'
DISPATCH = 'objectives/anti-static/obfuscation/control-flow/dispatch::native-addon-abi-mismatch-encoded-state-dispatch'

CASES = [
    (HERE / 'legacy-fsevents.node', {WATCH, ABI}, {MISMATCH}),
    (HERE / 'imports.node', {WATCH, ABI}, {MISMATCH}),
    (HERE / 'quoted-names.node', set(), {WATCH, ABI}),
    (HERE / 'local-definition.node', set(), {WATCH, ABI}),
    (HERE / 'unrelated-namespace.node', {MISMATCH}, {WATCH, ABI}),
    (HERE.parent / 'vsix-triage-2026-10-20' / 'ordinary-native-addon.node',
     {'metadata/binary/symbols/abi-name::node-native-abi-name-reference'}, {MISMATCH}),
    (HERE.parent / 'vsix-triage-2026-10-20' / 'native-import-iife.vsix',
     {STARTUP, MISMATCH}, {ABI}),
    (HERE.parent / 'vsix-triage-2026-10-20' / 'native-abi-mismatch.vsix',
     {STARTUP, DISPATCH, MISMATCH}, {ABI}),
]

for path, required, forbidden in CASES:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert required <= ids, (path.name, 'missing', sorted(required - ids))
    assert not forbidden & ids, (path.name, 'unexpected', sorted(forbidden & ids))
    print('PASS', path.name)
