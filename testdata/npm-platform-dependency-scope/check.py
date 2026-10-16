"""Separate manifest identity, optional dependency names and native contents."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
prefix = 'metadata/package/dependencies/manifest/name-form::'
platform_ids = {p: prefix + 'optional-platform-' + p + '-dep-name'
                for p in ['linux', 'darwin', 'windows']}
cases = [
    ('own-name-only', {'name': 'demo-darwin-arm64'}, set()),
    ('description-only', {'name': 'demo', 'description': 'demo-linux-x64'}, set()),
    ('ordinary-dependency', {'name': 'demo', 'dependencies': {'demo-linux-x64': '1.0.0'}}, set()),
    ('unrelated-optional', {'name': 'demo-darwin-arm64', 'optionalDependencies': {'safe': '1.0.0'}}, set()),
    ('version-value-is-not-a-name', {'name': 'demo', 'optionalDependencies': {'safe': 'demo-darwin-arm64'}}, set()),
    ('optional-darwin', {'name': 'demo', 'optionalDependencies': {'demo-darwin-arm64': '1.0.0'}}, {'darwin'}),
    ('optional-linux', {'name': 'demo', 'optionalDependencies': {'@scope/demo-linux-x64-musl': '1.0.0'}}, {'linux'}),
    ('optional-windows', {'name': 'demo', 'optionalDependencies': {'demo-win32-arm64-msvc': '1.0.0'}}, {'windows'}),
]
with tempfile.TemporaryDirectory(prefix='npm-platform-scope-') as tmp:
    root = Path(tmp)
    for name, manifest, _ in cases:
        path = root / name / 'package.json'
        path.parent.mkdir()
        path.write_text(json.dumps({'version': '1.0.0', 'license': 'MIT', **manifest}))
    run = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json', str(root)],
                         text=True, capture_output=True, check=True)
    text = run.stdout
    decoder = json.JSONDecoder()
    files = []
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        files.extend(report['files'])
        text = text.lstrip()[end:]
    for name, _, expected in cases:
        file = next(f for f in files if f['path'].endswith('/' + name + '/package.json'))
        matched = {t['id'] for t in file.get('traits', [])}
        actual = {p for p, id in platform_ids.items() if id in matched}
        assert actual == expected, (name, actual, expected)
        assert (prefix + 'platform-optional-deps' in matched) == bool(expected), name
print(f'{len(cases)} platform dependency scope cases passed')
