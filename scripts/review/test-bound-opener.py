#!/usr/bin/env python3
"""Check detached opener exceptions against bound and unrelated children."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RULE = 'micro-behaviors/process/create/shellexec::node-detached-os-default-handler-spawn'
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')

helper = """const {spawn} = require('child_process');
function launch(cmd, url) { return spawn(cmd, [url], {detached:true, stdio:'ignore'}).unref(); }
function openUrl(url) { const selected = process.platform === 'darwin' ? 'open' : 'xdg-open'; return launch(selected, url); }
"""
unrelated = """const {spawn} = require('child_process');
const documentation = ['open', 'xdg-open'];
spawn('node', ['worker.js'], {detached:true, stdio:'ignore'}).unref();
"""

with tempfile.TemporaryDirectory(prefix='bound-opener-') as temp:
    work = Path(temp)
    cases = []
    for name, source, expected in (
        ('helper', helper, True),
        ('helper-unbound', helper.replace('spawn(cmd,', 'spawn("node",'), False),
        ('unrelated-worker', unrelated, False),
        ('direct', "spawn('xdg-open', [url], {detached:true, stdio:'ignore'}).unref();\n", True),
        ('wrong-rundll', "spawn('rundll32', ['other.dll,Entry', url], {detached:true, stdio:'ignore'}).unref();\n", False),
    ):
        path = work / (name + '.js')
        path.write_text(source)
        cases.append((name, path, expected))
    for name in ('detached-browser-open-upgrade-controls.js', 'shell-true-comment-controls.js'):
        cases.append((name, ROOT / 'testdata/notable/controls' / name, True))
    original = (ROOT / 'testdata/notable/controls/shell-true-comment-controls.js').read_text()
    wrong_child = work / 'wrong-child.js'
    wrong_child.write_text(original.replace('child.unref();', 'another.unref();'))
    cases.append(('wrong-child', wrong_child, False))

    for name, path, expected in cases:
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', RULE, str(path)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        summary = 'Summary: 1 matched, 0 not matched' if expected else 'Summary: 0 matched, 1 not matched'
        if summary not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
