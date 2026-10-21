"""Check that API calls and argv differ from names stored in ordinary data."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
here = Path(__file__).resolve().parent
http = 'micro-behaviors/communications/http/'
handler = http + 'authorization-header::python-http-basic-auth-handler'
servers = {http + 'server/framework::' + name for name in (
    'http-server-module', 'simplehttpserver-module', 'basehttpserver-module')}
argv = 'micro-behaviors/process/argument/subcommand::cli-verb-print'
identity = 'well-known/lib/stdlib/six::six-compatibility-module'
reflection = 'micro-behaviors/metaprogramming/reflection::python-getattr-call'
expected = {
    'calls.py': ({handler, argv} | servers, {identity}),
    'references.py': ({reflection}, {handler, argv, identity} | servers),
    'six-names-in-string.py': (set(), {identity}),
    'incomplete-six.py': (set(), {identity}),
}
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--format',
     'json', *[str(here / name) for name in expected]],
    check=True, text=True, capture_output=True,
)
remaining = result.stdout
seen = set()
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report.get('files', [report]):
        name = Path(file['path']).name
        if name not in expected:
            continue
        seen.add(name)
        ids = {trait['id'] for trait in file['traits']}
        yes, no = expected[name]
        assert yes <= ids, (name, 'missing', yes - ids)
        assert not no & ids, (name, 'unexpected', no & ids)
assert seen == set(expected), ('missing reports', set(expected) - seen)
print('PASS: real calls, string-only references, and six identity near misses')
