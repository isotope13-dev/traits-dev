#!/usr/bin/env python3
"""Keep inline process calls and configured package scripts visible in context."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='node-inline-') as tmp:
    root = Path(tmp)
    cases = {
        'entry.js': 'spawn("node", ["-e", code]);\n',
        'entry.test.js': 'describe("case", () => spawn("node", ["-e", code]));\n',
        'computed.js': 'cp["spawn"]("node", ["-e", code]);\n',
        'literal.js': 'const note = "spawn(\\"node\\", [\\"-e\\", code])";\n',
        'package.json': json.dumps({'name': 'fixture', 'version': '1.0.0', 'scripts': {
            'preinstall': 'node -e "runCode()"', 'postinstall': 'node -e "fs.mkdirSync(\"a\")"'}}),
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
    direct = 'micro-behaviors/process/deploy/interpreter-command::spawn-node-eval'
    computed = 'micro-behaviors/process/deploy/interpreter-command::spawn-node-eval-computed-access'
    manifest = 'metadata/package/scripts/inline::manifest-node-inline-command'
    assert direct in ids['entry.js'] and direct in ids['entry.test.js'], ids
    assert computed in ids['computed.js'], ids['computed.js']
    assert direct not in ids['literal.js'] and computed not in ids['literal.js'], ids['literal.js']
    assert manifest in ids['package.json'], ids['package.json']
    print('Node calls and package commands remain visible without test-context suppression.')
