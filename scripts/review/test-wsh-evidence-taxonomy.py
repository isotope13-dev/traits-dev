#!/usr/bin/env python3
"""Verify ReadyState context and WScript loop observations after migration."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='wsh-evidence-') as tmp:
    root = Path(tmp)
    cases = {
        'ready.js': 'const marker = () => 0;\ndo { if (xhr.readyState < 4) continue; WScript.Sleep(5); } while (waiting);\n',
        'while.js': 'const marker = () => 0;\nwhile (counter < 4) { WScript.Sleep(5); }\n',
        'negative.js': 'const marker = () => 0;\ndo { if (xhr.status < 4) continue; WScript.Sleep(5); } while (waiting);\n',
    }
    for name, source in cases.items():(root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    profile = 'metadata/lang/source/syntax/control-flow::do-while-readystate-host-clues'
    loop = 'micro-behaviors/data/control-flow/loop/conditional::wscript-while-less-four-text'
    assert set(ids) == set(cases), ids.keys()
    assert profile in ids['ready.js'] and profile not in ids['negative.js'], ids
    assert loop in ids['while.js'], ids['while.js']
    print('ReadyState host clues and generic WScript loops retain distinct homes.')
