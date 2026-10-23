#!/usr/bin/env python3
"""Check saved scans; never compile or execute the native fixtures.
Usage: check.py SCRATCH_REVIEW_DIRECTORY
The controls are copied outside testdata before scanning so path exclusions do
not mask the source-map rule. Reports may contain concatenated JSON documents.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])

def documents(path):
    text = path.read_text()
    decoder = json.JSONDecoder()
    while text.strip():
        item, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield item

def files(path):
    return {Path(f['path']).name: f for j in documents(path)
            for f in j.get('raw', j).get('files', [])}

def ids(file, minimum=0):
    return {t['id'] for t in file['traits'] if t['crit'] >= minimum}

before = files(root / 'controls.before.json')
after = files(root / 'controls.final.json')
c2 = 'objectives/command-and-control/channel/deaddrop/blockchain::solana-account-data-c2-resolution'
execute = 'objectives/execution/payload/module-load::blockchain-resolved-coff-module-execution'
http = 'micro-behaviors/communications/http/url/build::native-decoded-response-authority'
coff = 'micro-behaviors/process/deploy/module-load::http-coff-rwx-symbol-entry-call'
comment = 'objectives/anti-static/obfuscation/obfuscator/js-obfuscator::source-map-comment-with-rc4-obfuscator'
for name in ['coff-dead-drop.c', 'coff-renamed.c']:
    assert {c2, execute, http, coff} <= ids(after[name]), name
for name in ['coff-local-module.c', 'coff-no-entry-call.c', 'coff-unrelated-authority.c']:
    assert not ids(after[name], 5), name
assert coff not in ids(after['coff-no-entry-call.c'])
assert http in ids(after['coff-no-entry-call.c'])
assert http not in ids(after['coff-unrelated-authority.c'])
assert coff in ids(after['coff-unrelated-authority.c'])
assert comment in ids(after['ordinary-map-rc4-comment.js'], 4)
assert not ids(after['ordinary-map-rc4-comment.js'], 5)
assert comment in ids(after['ndsj-comment-tail.js'], 4)
assert comment not in ids(after['ndsj-active-payload.js'])
assert 'micro-behaviors/data/encoding/xor::c-xor-assign-modulo-operand' in ids(after['xor-assignment.c'])
assert 'micro-behaviors/data/encoding/xor::c-xor-assign-modulo-operand' not in ids(after['xor-scalar.c'])
assert 'micro-behaviors/data/arithmetic::native-xor-modulo-arithmetic' in ids(after['go-ws-unmask-controls.go'])
assert not ids(after['go-ws-unmask-controls.go'], 4)
# Preserve independent, pre-existing attacks outside the reviewed samples.
for name in ['rc4-table-gate-loader.html', 'ethereum-deaddrop-live-rpc.js',
             'compressed-source-evaluation.py', 'hidden-rc4-stage.js']:
    assert ids(before[name], 4) <= ids(after[name], 4), name
assert not ids(after['compact-rpc-base64-client.mjs'], 4)
# Original specimens: all PE detections remain; native intent still has two
# separate supported results; JS retains every original suspicious observation.
for name in ['pe', 'c', 'js']:
    old = list(files(root / (name + '.before.json')).values())[0]
    new = list(files(root / (name + '.after.json')).values())[0]
    assert len(files(root / (name + '.after.json'))) == 1
    if name == 'pe':
        assert ids(old) == ids(new)
        assert len(ids(new, 5)) >= 2
    elif name == 'c':
        assert {c2, execute} <= ids(new, 5)
    else:
        assert {t['id'] for t in old['traits'] if t['crit'] == 4} <= ids(new, 4)
        assert comment in ids(new, 4)
        assert not ids(new, 5)
print('PASS: bound native chains, renamed entry, benign controls, retained attacks, and all original findings accounted for')
