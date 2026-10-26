#!/usr/bin/env python3
"""Check linked URL, deployment and response-stream placement boundaries."""
import json
from pathlib import Path
import sys

def files(path):
    source = Path(path).read_text()
    decoder = json.JSONDecoder()
    result = {}
    while source.strip():
        source = source.lstrip()
        report, used = decoder.raw_decode(source)
        source = source[used:]
        for file in report['files']:
            result[file['path']] = {t['id'] for t in file.get('traits', [])}
    return result

actual = files(sys.argv[1])
chain = 'objectives/execution/payload/file-exec::python-discord-appdata-hidden-dropper'
wheel = 'objectives/execution/payload/file-exec::wheel-console-script-discord-dropper'
get = 'micro-behaviors/communications/http/get::python-helper-get-discord-executable-url'
stream = 'micro-behaviors/communications/http/client/response-body::response-stream-python'
for path, traits in actual.items():
    name = Path(path).name
    if name in {'linked.py', 'renamed.py'}:
        assert {chain, get, stream} <= traits, path
    if name in {'unrelated-discord.py', 'wrong-request-parameter.py', 'different-exec.py', 'visible.py'}:
        assert chain not in traits, path
    if name == 'unrelated-discord.py':
        assert get not in traits and stream in traits, path
    if name == 'linked.whl':
        assert {chain, wheel} <= traits, path
    if name == 'unrelated-discord.whl':
        assert not {chain, wheel} & traits, path
    if name == 'stream-syntax.py':
        assert stream in traits, path
    if name == 'near-stream-far-request.py':
        assert 'objectives/command-and-control/beacon/tracking::generic-tracking-pixel-beacon' in traits, path
    if name == 'far-stream-and-request.py':
        assert 'objectives/command-and-control/beacon/tracking::generic-tracking-pixel-beacon' not in traits, path
    if name == 'nonstream.py':
        assert stream not in traits, path
print('PASS linked, renamed, unrelated URL, wrong argument, launch and stream controls')
