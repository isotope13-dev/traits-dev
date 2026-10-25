#!/usr/bin/env python3
"""Check the saved cleave JSONL report for the source boundary controls."""
import json
import pathlib
import sys

launch = 'micro-behaviors/process/create/subprocess::swift-source-process-run'
file_write = 'micro-behaviors/fs/write/file/full::swift-file-write-destination'
permission = 'micro-behaviors/fs/chmod/modify::swift-directory-posix-permissions'
directory = 'micro-behaviors/fs/directory/create::swift-create-directory-call'
unix_socket = 'micro-behaviors/communications/ipc/unix-socket::swift-unix-socket-create'
ipc = {
    unix_socket, permission, directory,
    'micro-behaviors/communications/socket/send::swift-darwin-send-call',
    'micro-behaviors/communications/socket/receive::swift-darwin-recv-call',
    'micro-behaviors/data/parse/json::swift-jsondecoder-decode',
    'micro-behaviors/data/serialize/json::swift-jsonencoder-encode',
    'micro-behaviors/os/security/policy::swift-secure-event-input-query',
}
new_rules = ipc | {launch, file_write}
expected = {
    'launch.swift': ({launch}, set()),
    'nested-launch.swift': ({launch}, set()),
    'commented-launch.swift': (set(), {launch}),
    'different-receiver.swift': (set(), {launch}),
    'comments.swift': (set(), new_rules),
    'file-write.swift': ({file_write}, {launch}),
    'ipc.swift': (ipc, {launch, file_write,
                          'micro-behaviors/fs/write/file/full::source-buffer-write-call'}),
    'no-permission.swift': ({directory}, {permission, unix_socket}),
    'ruby-references.rb': ({
        'metadata/lang/source/syntax/member::ruby-file-write-reference',
        'micro-behaviors/data/parse/json::ruby-json-parse-call',
        'micro-behaviors/data/serialize/json::ruby-json-pretty-generate',
    }, set()),
}
seen = set()
# Split only at ASCII newline: binary contexts may contain Unicode separators.
for line in pathlib.Path(sys.argv[1]).read_text().split('\n'):
    if not line:
        continue
    for entry in json.loads(line)['files']:
        name = pathlib.Path(entry['path']).name
        if name not in expected:
            continue
        seen.add(name)
        actual = {t['id'] for t in entry.get('traits', [])}
        present, absent = expected[name]
        assert present <= actual, (name, 'missing', present - actual)
        assert not absent & actual, (name, 'unexpected', absent & actual)
assert seen == set(expected), ('unscanned controls', set(expected) - seen)
print(f'{len(seen)} source boundary controls passed')
