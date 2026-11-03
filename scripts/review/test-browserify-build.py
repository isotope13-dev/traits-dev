#!/usr/bin/env python3
"""Check Browserify build recognition without confusing filenames for commands."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
bundler = 'metadata/package/scripts/build::script-runs-bundler-cli'
phantom = 'objectives/supply-chain/hidden-payload/staging/loader::phantom-dist-directory'
cases = {
    'build': ('mkdir -p dist && browserify -s library index.js | uglifyjs -c > dist/library.js', True),
    'filename': ('node browserify.config.js', False),
}
with tempfile.TemporaryDirectory(prefix='browserify-build-') as tmp:
    paths = []
    for name, (script, _) in cases.items():
        path = Path(tmp) / name / 'package.json'
        path.parent.mkdir()
        path.write_text(json.dumps({'name': name, 'version': '1.0.0', 'files': ['dist/'], 'main': 'index.js', 'scripts': {'prepublishOnly': script}}))
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        file = json.loads(line)['files'][0]
        name = Path(file['path']).parent.name
        ids = {t['id'] for t in file.get('traits', [])}
        assert (bundler in ids) == cases[name][1], (name, ids)
        if name == 'build':
            assert phantom not in ids, ids
        else:
            finding = next(t for t in file.get('traits', []) if t['id'] == phantom)
            assert finding['crit'] == 3, finding
        seen.add(name)
    assert seen == set(cases), seen
print('Browserify build boundaries passed.')
