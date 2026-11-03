#!/usr/bin/env python3
"""Keep interpreter calls and unbound source-input clues in separate homes."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='interpreter-input-') as tmp:
    root = Path(tmp)
    cases = {
        'input.py': 'import subprocess\nsubprocess.run("python", input=source)\n',
        'list.py': 'import subprocess\nsubprocess.run(["python", "-c", code], input=source)\n',
        'argument.py': 'import subprocess\nsubprocess.run(["echo", "python"])\n',
        'input.js': 'cp.spawn("lua", [source]);\n',
        'unrelated.py': 'import subprocess\nsubprocess.run("python")\n',
        'unrelated.js': 'cp.spawn("lua", [other]);\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    pycall = 'metadata/file/profile/process/creation-api::interpreter-name-a'
    pylist = 'metadata/file/profile/process/creation-api::interpreter-name-list'
    jscall = 'micro-behaviors/process/interpreter/lua::javascript-interpreter-name'
    pyprofile = 'metadata/file/profile/script/evaluation::python-source-interpreter-input-clues'
    jsprofile = 'metadata/file/profile/script/evaluation::javascript-lua-source-call-clues'
    assert pycall in ids['input.py'] and pyprofile in ids['input.py'], ids['input.py']
    assert pylist in ids['list.py'] and pyprofile in ids['list.py'], ids['list.py']
    assert pylist not in ids['argument.py'], ids['argument.py']
    assert jscall in ids['input.js'] and jsprofile in ids['input.js'], ids['input.js']
    assert pycall in ids['unrelated.py'] and pyprofile not in ids['unrelated.py'], ids['unrelated.py']
    assert jscall in ids['unrelated.js'] and jsprofile not in ids['unrelated.js'], ids['unrelated.js']
    print('Interpreter calls and input clues retain their distinct evidence.')
