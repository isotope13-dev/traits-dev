#!/usr/bin/env python3
"""Do not confuse helper names ending in Function with dynamic evaluators."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/process/interpreter/eval/constructed::dynamic-evaluator-identifier-argument'
cases = {
    'function.js': ('Function(payload);\n', True),
    'indirect.js': ('(0, eval)(payload);\n', True),
    'method.js': ('obj.constructor(payload);\n', True),
    'helper.js': ('if (isFunction(output)) output.apply(mom);\n', False),
    'identifier.js': ('notFunction(payload);\n', False),
}
with tempfile.TemporaryDirectory(prefix='dynamic-evaluator-boundary-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(source)
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        file = json.loads(line)['files'][0]
        name = Path(file['path']).name
        actual = any(t['id'] == trait for t in file.get('traits', []))
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('Dynamic evaluator identifier boundaries passed.')
