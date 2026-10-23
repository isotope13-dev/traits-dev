#!/usr/bin/env python3
"""Focused trait controls; fixture payloads are read, never executed."""
import json
import os
from pathlib import Path
import subprocess
import re
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
mb = 'micro-behaviors/'
meta = 'metadata/'
button = mb + 'ui/controls/button::play-listen-markup-label'
marker = mb + 'crypto/hash/mining::mining-marker'
mining = mb + 'crypto/hash/mining::mining-memory-worker-markers'
hardware = mb + 'crypto/hash/mining::mining-hardware-markers'
evaluation = mb + 'process/interpreter/eval/direct::base64-evaluation-call-text'
compile_call = mb + 'process/interpreter/eval/compile::base64-compile-call-text'
source = mb + 'process/interpreter/eval/source::shell-source-command'
url = mb + 'communications/http/url/path::script-url-reference-pe'
name = meta + 'file/naming::business-document-themed-basename'
controls = {
    'action.html': ([button], []),
    'manual.html': ([meta + 'document/html::groff-creator-comment',
                     meta + 'lang/natural::en-shell-backdoor-term'], [button]),
    'plain.html': ([], [button, meta + 'document/html::groff-creator-comment']),
    'options.sh': ([mb + 'process/argument/option::xmrig-randomx-mode-option',
                    mb + 'process/argument/option::xmrig-cpu-threads-hint-option',
                    mb + 'process/argument/option::xmrig-algo-randomx-option'], []),
    'mining.sh': ([marker, mining, hardware], []),
    'hugepages.sh': ([], [marker, mining, hardware]),
    'algorithm.sh': ([marker], [mining, hardware]),
    'encoded-eval.py': ([evaluation], [compile_call]),
    'encoded-exec.py': ([evaluation], [compile_call]),
    'encoded-compile.py': ([compile_call], [evaluation]),
    'encoded-method.py': ([], [evaluation, compile_call]),
    'encoded-near-identifier.py': ([], [evaluation, compile_call]),
    'encoded-both.py': ([evaluation], [compile_call]),
    'invoice-sign.exe': ([name, url], []),
    'utility.exe': ([url], [name]),
    'source.sh': ([source], []),
    'source-prose.sh': ([], [source]),
}
controls['signedxml.exe'] = ([mb + 'crypto/sign::dotnet-xml-digital-signature'], [])
controls['signedxml-type.exe'] = ([], [mb + 'crypto/sign::dotnet-xml-digital-signature'])

def check(item):
    filename, (matched, absent) = item
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             'test-rules', str(HERE / filename), '--rules',
                             ','.join(matched + absent)], capture_output=True, text=True, check=True)
    output = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout + result.stderr)
    detected = set(re.findall(r'^MATCHED (\S+)', output, re.MULTILINE))
    errors = [f'{filename}: missing {t}' for t in matched if t not in detected]
    errors += [f'{filename}: unexpected {t}' for t in absent if t in detected]
    return errors

if sys.argv[1:]:
    controls = {name: controls[name] for name in sys.argv[1:]}

with ThreadPoolExecutor(max_workers=4) as pool:
    failures = [error for errors in pool.map(check, controls.items()) for error in errors]
if failures:
    raise SystemExit('\n'.join(failures))
print(f'{len(controls)} focused controls passed')
