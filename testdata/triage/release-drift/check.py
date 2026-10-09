"""Check atomscan JSONL from this directory's release-drift controls."""
import json
import pathlib
import sys

root = pathlib.Path(__file__).parent
expected = {
    'http-yaml.py': ('yaml-load-near-http-client-unspecified-loader', True),
    'local-yaml.py': ('yaml-load-near-http-client-unspecified-loader', False),
    'build-task.targets': ('msbuild-property-task-with-precompile-target', True),
    'task-only.targets': ('msbuild-property-task-with-precompile-target', False),
    'commented-task.targets': ('msbuild-property-task-with-precompile-target', False),
    'override-live.py': ('llm-ignore-prior-instructions-literal', True),
    'assigned-triple-prompt.py': ('llm-ignore-prior-instructions-literal', True),
    'override-doc.py': ('llm-ignore-prior-instructions-literal', False),
}
seen = set()
for line in pathlib.Path(sys.argv[1]).read_text().splitlines():
    report = json.loads(line)
    for file in report['raw']['files']:
        name = pathlib.Path(file['path']).name
        if name not in expected:
            continue
        trait, should_match = expected[name]
        matches = [t for t in file.get('traits', [])
                   if t['id'].endswith('::' + trait)]
        assert bool(matches) == should_match, (name, trait, matches)
        assert all(t['crit'] == 3 for t in matches), (name, matches)
        seen.add(name)
assert seen == set(expected), ('missing controls', set(expected) - seen)
print('All eight release-drift controls passed')
