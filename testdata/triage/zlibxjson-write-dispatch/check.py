"""Compare preserved rule coverage across the write/dispatch placements."""
import json
from pathlib import Path
import sys

MOVES = {
    'micro-behaviors/process/io/stream::python-write-method-call':
        'micro-behaviors/data/control-flow/dispatch::python-write-method-call',
    'micro-behaviors/process/io/stream::python-file-or-stream-write':
        'micro-behaviors/data/control-flow/dispatch::python-write-call-observation',
    'micro-behaviors/data/control-flow/dispatch::exec-method-call-text':
        'metadata/lang/source/syntax/call/invocation::exec-method-call-text',
    'micro-behaviors/data/control-flow/dispatch::send-method-call-text':
        'metadata/lang/source/syntax/call/invocation::send-method-call-text',
}


def reports(path):
    source = Path(path).read_text()
    decoder = json.JSONDecoder()
    result = {}
    while source.strip():
        source = source.lstrip()
        report, consumed = decoder.raw_decode(source)
        source = source[consumed:]
        for file in report.get('raw', report)['files']:
            result[file['path']] = {
                MOVES.get(t['id'], t['id']): t['crit']
                for t in file.get('traits', [])
            }
    return result


after = reports(sys.argv[1])
checked = 0
for before_path in sys.argv[2:]:
    for path, expected in reports(before_path).items():
        assert path in after, path
        assert expected == after[path], (path, expected.items() - after[path].items(),
                                         after[path].items() - expected.items())
        checked += 1
write = MOVES['micro-behaviors/process/io/stream::python-write-method-call']
for path, traits in after.items():
    if path.endswith('/custom-writer.py'):
        # Unreferenced baseline observations are stripped by the renderer.
        assert not any(t.startswith('micro-behaviors/fs/write/') for t in traits), traits
    if path.endswith('/name-only.py'):
        assert write not in traits, traits
print(f'Preserved all findings and criticalities in {checked} fixture reports')
