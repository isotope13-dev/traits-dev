"""Check saved full scans and source-specific mutation controls.

Usage: python3 testdata/surveillance-xcitium-review/check.py SCRATCH
The scratch directory contains original Atomscan JSON, not verdict fixtures.
"""
import collections
import json
from pathlib import Path
import sys

s = Path(sys.argv[1])
window = 'objectives/collection/keylog/hook::dotnet-keylogger-window-title-profile'
cookie = 'objectives/exfiltration/stealer/browser::managed-keylogger-cookie-record-upload-profile'

def read(name):
    return json.loads((s / name).read_text())

def traits(report):
    return {t['id']: t['crit'] for f in report['raw']['files'] for t in f.get('traits', [])}

def counts(report):
    ts = traits(report)
    return [sum(v == 5 for v in ts.values()), sum(v == 4 for v in ts.values())]

expected = [([34, 12], [36, 12]), ([2, 3], [2, 3]), ([4, 6], [0, 1])]
for i, (before, after) in enumerate(expected):
    a = read(f'{i}.scan.before.json')
    b = read(f'{i}.after.json')
    assert counts(a) == before, (i, counts(a))
    assert counts(b) == after, (i, counts(b))
    if i < 2:
        aa, bb = traits(a), traits(b)
        assert all(bb.get(k) == v for k, v in aa.items()), i
    else:
        aa, bb = traits(a), traits(b)
        mapping = read('migration.json')['mapping']
        assert all(k in bb or mapping.get(k) in bb for k in aa), set(aa) - set(bb)
        assert 'objectives/discovery/host/security::pe-wmi-av-enumeration' in bb
        assert len(a['raw']['files']) == len(b['raw']['files']) == 2

base = traits(read('0.after.json'))
assert base[window] == base[cookie] == 5
nw = traits(read('no-window-title.json'))
nc = traits(read('no-cookie-record.json'))
assert window not in nw and nw[cookie] == 5
assert cookie not in nc and nc[window] == 5
for control in ['positive', 'mettle', 'native-stager', 'sibling-managed']:
    assert traits(read(control + '.before.json')) == traits(read(control + '.after.json')), control
print('PASS: all sample deltas, both source-specific controls, four external controls')
