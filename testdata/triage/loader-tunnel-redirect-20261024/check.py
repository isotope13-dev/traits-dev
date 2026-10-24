#!/usr/bin/env python3
"""Check bootstrap path/source binding and retained module/tunnel observations."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
BOOT = 'micro-behaviors/process/deploy/file-exec::python-written-bootstrap-interpreter'
MOD = 'micro-behaviors/os/module/load::'
CLOUD = MOD + 'cloudflared-node-package-require'
QUICK = 'micro-behaviors/communications/proxy/tunnel::cloudflared-node-quick-tunnel'
CASES = [
    ('remote-runner.py', [BOOT, MOD+'python-spec-from-file-location', MOD+'python-loaded-module-exec-module'], []),
    ('renamed-runner.py', [BOOT], []),
    ('local-job-runner.py', [BOOT], []),
    ('different-launch-path.py', [], [BOOT]),
    ('different-write-source.py', [], [BOOT]),
    ('unrelated-network-module.py', [MOD+'python-loaded-module-exec-module'], [BOOT]),
    ('literal-loader.py', [MOD+'python-spec-from-file-location', MOD+'python-loaded-module-exec-module'], []),
    ('cloudflared-module.js', [CLOUD], [QUICK]),
    ('cloudflared-tunnel.js', [CLOUD, QUICK], []),
]
run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--format', 'jsonl', *[str(ROOT/f) for f, _, _ in CASES]], env={**os.environ, 'CLEAVE_VALIDATE': '0'}, text=True, capture_output=True, check=True)
decoder = json.JSONDecoder()
remaining = run.stdout.lstrip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    files.update({Path(f['path']).name: {t['id'] for t in f.get('traits', [])} for f in report['files'] if f.get('type') in ('python', 'javascript')})
results = []
for name, required, forbidden in CASES:
    ids = files[name]
    missing = sorted(set(required)-ids)
    unexpected = sorted(set(forbidden)&ids)
    old = [t for t in ids if t.startswith('micro-behaviors/os/api-resolution/dynamic::python-')]
    assert not (missing or unexpected or old), (name, missing, unexpected, old)
    results.append({'file': name, 'passed': True, 'required': required, 'forbidden': forbidden})
print(json.dumps(results, indent=2))
