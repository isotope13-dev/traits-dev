#!/usr/bin/env python3
"""Verify the saved independent scans; pass their scratch directory as argv[1]."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
objective = 'objectives/persistence/system/service/install::hidden-resource-injector-auto-service'
layout = 'micro-behaviors/os/service/create::x86-auto-own-process-service-call-layout'
decoder = 'micro-behaviors/data/decode/base64::jvm-base64-static-decode-source-call'

def read(name):
    return json.loads((root / name).read_text())

def findings(report):
    return {f['path']: {t['id']: t['crit'] for t in f.get('traits', [])}
            for f in report['raw']['files']}

for index in range(3):
    before = read(f'before-{index}.json')
    after = read(f'final-{index}.json')
    old, new = findings(before), findings(after)
    for path, traits in old.items():
        for name, severity in traits.items():
            assert new[path].get(name) == severity, (path, name)
    additions = {(path, name) for path, traits in new.items()
                 for name in traits.keys() - old.get(path, {}).keys()}
    assert len(additions) == [2, 0, 1][index], additions
    assert {name for _, name in additions} == [{objective, layout}, set(), {decoder}][index]
    for field in ['prob', 'lvl', 'conf']:
        assert before['ml'][field] == after['ml'][field], (index, field)
    if index != 0:
        assert before['ml']['mods'] == after['ml']['mods']

for line in (root / 'controls-after.jsonl').read_text().splitlines():
    report = json.loads(line)
    f = report['raw']['files'][0]
    name = Path(f['path']).name
    ids = {t['id'] for t in f.get('traits', [])}
    assert objective not in ids, name
    assert (layout in ids) == (name in {
        'visible-install.exe', 'no-service-api.exe', 'service-layout-only.exe'
    }), name
    if name.endswith(('.jsp', '.java')):
        assert (decoder in ids) == ('name-only' not in name), name

assert findings(read('sweetalert2-before.json')) == findings(read('sweetalert2-final.json'))
assert len(read('regional-trace.json')['cases']) == 8
print('PASS: all prior detections retained; expected additions only; 8 controls; 8 regional cases; dependency unchanged')
