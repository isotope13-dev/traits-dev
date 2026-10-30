#!/usr/bin/env python3
"""Check query contents, operations and the limits of unbound name evidence."""
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
URL = 'micro-behaviors/communications/url/'
CASES = {
    'credential.js': 'const endpoint = "https://service.example.net/?token=abcdefghijklmnop";\n',
    'prompt.js': 'const endpoint = "https://service.example.net/?prompt=look&next=https://remote.example.net/picture.png";\n',
    'construct.js': 'const params = new URLSearchParams();\nparams.append("next", item);\nconst url = "https://service.example.net/?data=" + encodeURIComponent(item);\n',
    'computed.js': 'targetUrl[prefix + "ms"][operation](value);\n',
    'properties.js': 'const settings = {unique: true, ttl: 30, R_PATH: "/handoff"};\n',
    'lookup.js': "const code = params.get('code');\n",
    'parse.js': 'const token = new URLSearchParams(uri.query).get("token");\n',
    'encoded.py': 'endpoint = ' + repr(base64.b64encode(b'https://remote.example.net/api').decode()) + '\n',
    'typed_data.js': 'const endpoint = `https://service.example.net/?type=${kind}&data=${payload}`;\n',
}
EXPECTED = {
    'credential.js': {URL + 'query/credential::token-query-parameter'},
    'prompt.js': {URL + 'query/prompt::prompt-query-key-basic', URL + 'query/endpoint::nested-remote-url-value'},
    'construct.js': {URL + 'construction/query::js-urlsearchparams-construction', URL + 'construction/query::query-parameter-mutation', URL + 'construction/query::encoded-query-parameter'},
    'computed.js': {'micro-behaviors/data/control-flow/dispatch/computed::computed-target-url-params-call'},
    'properties.js': {'metadata/lang/source/syntax/key-value::unique-ttl-r-path-field-context'},
    'lookup.js': {'metadata/lang/source/syntax/call/arguments::params-code-lookup'},
    'parse.js': {URL + 'parse::url-search-params', URL + 'parse::uri-token-param'},
    'encoded.py': {URL + 'encoded::base64-decoded-http-url'},
    'typed_data.js': {URL + 'construction/query::interpolated-type-data-query'},
}

with tempfile.TemporaryDirectory(prefix='query-subject-boundaries-') as temporary:
    paths = []
    for name, source in CASES.items():
        path = Path(temporary) / name
        path.write_text(source)
        paths.append(str(path))
    output = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', 'analyze', *paths], text=True, capture_output=True, check=True)
    found = {}
    for line in output.stdout.splitlines():
        for file in json.loads(line).get('files', []):
            found[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
    for name, expected in EXPECTED.items():
        assert expected <= found[name], (name, expected - found[name], found[name])
        assert not any(identifier.startswith(URL + 'http-query::') or identifier.startswith('micro-behaviors/communications/http/query::') for identifier in found[name]), name
    assert not any(identifier.startswith('well-known/app/publishing/keitaro::') for identifier in found['properties.js']), found['properties.js']
    assert URL + 'parse::uri-code-state-lookup-context' not in found['lookup.js'], found['lookup.js']
    assert not any(identifier.startswith(URL + 'construction/query::') for identifier in found['computed.js']), found['computed.js']
    assert not any(identifier.startswith('micro-behaviors/data/decode/') for identifier in found['encoded.py']), found['encoded.py']
    assert not any(identifier.startswith('objectives/exfiltration/') for identifier in found['typed_data.js']), found['typed_data.js']
print('Query subjects: credentials, prompts, construction, dispatch, names, parsing and encoded content passed')
