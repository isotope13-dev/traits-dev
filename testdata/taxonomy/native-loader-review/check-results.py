#!/usr/bin/env python3
"""Check recorded atomscan/cleave JSON for real samples and mutated near misses.

Usage: check-results.py REPORT_DIRECTORY
The report directory contains {d436,b330,6afd}.verified.json and
controls.after.json, generated with local traits and no reference fetching.
See review.txt for the mutations; none of the control files are executed.
"""
import json
import sys
from pathlib import Path

p = Path(sys.argv[1])
def files(path):
    data = path.read_text()
    decoder = json.JSONDecoder()
    while data.strip():
        data = data.lstrip()
        obj, end = decoder.raw_decode(data)
        yield from obj.get('raw', obj).get('files', [])
        data = data[end:]

def ids(file):
    return {x['id'] for x in file['traits']}

mirai = {
    'well-known/malware/botnet/mirai/http::mirai-native-loader-markers',
    'well-known/malware/botnet/mirai/http::mirai-native-http-downloader',
}
client = 'objectives/command-and-control/channel/http-beacon::mpress-mac-command-client'
payload = 'objectives/execution/payload/file-exec::xor-record-http-native-file-launcher'
for name in ('d436', 'b330', '6afd'):
    file = next(files(p / (name + '.verified.json')))
    assert sum(t['crit'] == 5 for t in file['traits']) >= 2, name
    if name == 'b330':
        assert {client, payload} <= ids(file)
        assert not any('malware/stealer/blihan' in x for x in ids(file))
    if name == '6afd':
        assert mirai <= ids(file)
        assert 'micro-behaviors/communications/http/download/executable::tiny-static-http-world-executable-file' in ids(file)

controls = {Path(f['path']).name: f for f in files(p / 'controls.after.json')}
for name in ('arm-no-status.elf', 'arm-no-completion.elf', 'arm-non-executable-mode.elf'):
    assert not mirai & ids(controls[name]), name
    assert not any(t['crit'] >= 4 for t in controls[name]['traits']), name
assert mirai <= ids(controls['arm-renamed-target.elf'])
assert not {client, payload} & ids(controls['pe-no-key64.exe'])
assert client in ids(controls['pe-no-handoff.exe'])
assert payload not in ids(controls['pe-no-handoff.exe'])
print('PASS: three original samples and six independent role/rename controls')
