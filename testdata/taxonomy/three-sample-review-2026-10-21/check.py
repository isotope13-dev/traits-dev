#!/usr/bin/env python3
"""Verify padding bounds, retained primitives, and independent attack fixtures."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PAD = 'objectives/anti-static/obfuscation/string/junking::vbs-interleaved-empty-literal-concat'
EVAL = 'micro-behaviors/process/interpreter/eval/direct::executeglobal-variable'
CHR = 'micro-behaviors/data/encode/char-code::dense-chr-construction'
OLD = {
    'objectives/execution/interpreter/vbscript/loader::chr-built-vbs-execute-loader',
    'objectives/execution/interpreter/vbscript/loader::chr-built-vbs-executeglobal-loader',
    'objectives/execution/interpreter/vbscript/loader::vbs-remote-response-executeglobal',
}

with tempfile.TemporaryDirectory(prefix='.controls-', dir=HERE) as temp:
    temp = Path(temp)
    for path in (HERE / 'fixtures').glob('*.vbs'):
        shutil.copyfile(path, temp / path.name)
    positives = [ROOT / 'testdata/hostile/wsh-chr-wrapper-response-exec.vbs',
                 ROOT / 'testdata/hostile/vbs-numeric-table-execute-loader.vbs']
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(temp), *map(str, positives)],
        capture_output=True, text=True,
    )
    assert result.returncode in (0, 1), result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout
    files = {}
    while remaining.strip():
        remaining = remaining.lstrip()
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:]
        files.update({Path(f['path']).name: f for f in report['files']})
    traits = {name: {t['id']: t['crit'] for t in f.get('traits', [])}
              for name, f in files.items()}
    assert PAD in traits['padded-vbs.vbs']
    for name in ['ordinary-concat.vbs', 'quoted-padding.vbs',
                 'unrelated-evaluation.vbs', 'unrelated-http-evaluation.vbs']:
        assert PAD not in traits[name], name
        assert not OLD.intersection(traits[name]), name
    assert traits['dense-local-loader.vbs'][EVAL] == 4
    assert traits['dense-local-loader.vbs'][CHR] == 3
    for path in positives:
        assert any(level == 5 for level in traits[path.name].values()), path
    print('PASS: padding bounds, retained construction/evaluation, two attack fixtures')
