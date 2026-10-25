#!/usr/bin/env python3
"""Behavioral boundary regressions; no payloads or commands are executed."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
P = 'micro-behaviors/process/deploy/script-eval::'
R = 'micro-behaviors/communications/proxy/relay::'
DLL = 'micro-behaviors/process/inject/dll::remote-thread-resolved-loadlibrary'
OFFSET = 'objectives/anti-static/obfuscation/encoding/arithmetic::offset-hex-decoder-beside-document-write'
RDS = 'objectives/execution/activex/com::rds-http-response-save-and-launch'
CASES = {
    'rds-save-launch.html': ({RDS}, set()),
    'rds-save-only.html': (set(), {RDS}),
    'resolved-loader.cpp': ({DLL}, set()),
    'unrelated-loader.cpp': (set(), {DLL}),
    'background-forward.cpp': ({R + 'tailcat-hidden-launch-clues'}, set()),
    'forward-comment.cpp': (set(), {R + 'tailcat-source-forward-peer'}),
    'comment-pipeline.js': (set(), {P + 'powershell-webrequest-to-iex-pipeline', P + 'powershell-webrequest-iex-command-literal'}),
    'command-pipeline.js': ({P + 'powershell-webrequest-iex-command-literal'}, set()),
    'real-pipeline.ps1': ({P + 'powershell-webrequest-iex-script-text'}, set()),
    'dll-path.cpp': ({'micro-behaviors/fs/path/library::environment-library-path'}, set()),
    'offset-writer.html': ({OFFSET}, set()),
    'plain-writer.html': (set(), {OFFSET}),
}
existing = [ROOT / p for p in (
    'testdata/hostile/clickfix-os-gated-verify.html',
    'testdata/hostile/rogue-av-rds-exit-hook.html',
    'testdata/hostile/clickfix-savedialog-iwr-cradle.html',
    'testdata/date-key-browser/rekeyed-rds.html',
    'testdata/date-key-browser/commented-rds.html',
    'testdata/benign/js-powershell-webclient-command-string.js',
    'testdata/benign/powershell-download-eval-comment.ps1',
)]
cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl', *map(str, [*(HERE / n for n in CASES), *existing])]
result = subprocess.run(cmd, check=True, text=True, capture_output=True)
if result.stderr:
    print(result.stderr, file=sys.stderr)
files = [f for line in result.stdout.splitlines() for f in json.loads(line)['files']]
if len(sys.argv) > 1:
    Path(sys.argv[1]).write_text(result.stdout)
for name, (required, forbidden) in CASES.items():
    f = next(f for f in files if f['path'] == str(HERE / name))
    ids = {t['id'] for t in f.get('traits', [])}
    assert required <= ids, (name, 'missing', required - ids)
    assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
    if name == 'background-forward.cpp':
        assert not any(t['crit'] >= 4 for t in f['traits']), name
for path in existing:
    f = next(f for f in files if f['path'] == str(path))
    if path.parent.name == 'hostile' or path.name == 'rekeyed-rds.html':
        assert any(t['crit'] == 5 for t in f.get('traits', [])), path
    if path.parent.name == 'benign':
        assert not any(t['crit'] >= 4 for t in f.get('traits', [])), path
print(f'Passed {len(CASES)} boundary cases and {len(existing)} existing controls.')
