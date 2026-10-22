"""Compare atomscan JSON, accounting explicitly for reviewed trait corrections."""
import argparse
import json
from pathlib import Path

MOVED = {
    'objectives/supply-chain/recon-exfil/runtime::pypi-wheel-pth-startup-host-recon-snapshot':
        'micro-behaviors/process/interpreter/python::wheel-pth-metadata-json-context',
    'objectives/anti-static/obfuscation/multi-layer::python-medium-base64-decode-exec':
        'objectives/anti-static/obfuscation/payload/encoded/exec::python-one-line-base64-exec-large-string',
    'metadata/file/data-blob::python-string-over-10k':
        'metadata/file/profile/string-population::python-string-at-least-10k',
    'objectives/anti-static/obfuscation/encoding/content::encoded-python-malware-pattern':
        'objectives/anti-static/obfuscation/encoding/content::encoded-python-execution-primitives',
}
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('reports', type=Path)
a = p.parse_args()
for name in ('3e9014ef6a18', '1745877fbb9a', '4fb7989a132f', 'dependency', 'windows'):
    before, after = [json.loads((a.reports / (name + '.' + phase + '.json')).read_text()) for phase in ('before', 'after')]
    oldfiles = {f['path']: f for f in before['raw']['files']}
    newfiles = {f['path']: f for f in after['raw']['files']}
    assert oldfiles.keys() == newfiles.keys(), name
    changes = []
    for path, old in oldfiles.items():
        new = newfiles[path]
        assert old.get('sha') == new.get('sha'), path
        expected = {MOVED.get(t['id'], t['id']):
                    (3 if t['id'] == next(iter(MOVED)) else t['crit'])
                    for t in old.get('traits', [])}
        actual = {t['id']: t['crit'] for t in new.get('traits', [])}
        # Report additions separately so they cannot mask a detection loss.
        lost = expected.keys() - actual.keys()
        added = actual.keys() - expected.keys()
        different = {k for k in expected.keys() & actual.keys() if expected[k] != actual[k]}
        assert not lost and not different, (name, path, sorted(lost), sorted(different))
        if added:
            changes.append({'path': path, 'added': sorted(added)})
        assert not any(t['id'] in MOVED for t in new.get('traits', [])), path
    wheel_before = next(f for f in oldfiles.values() if f['type'] == 'whl')
    wheel_after = next(f for f in newfiles.values() if f['type'] == 'whl')
    counts = lambda f: {str(crit): sum(t['crit'] == crit for t in f.get('traits', [])) for crit in (4, 5)}
    print(json.dumps({'sample': name, 'files': len(oldfiles), 'before_counts': counts(wheel_before),
                      'after_counts': counts(wheel_after), 'before_risk': wheel_before['risk'],
                      'after_risk': wheel_after['risk'], 'before_prob': before['ml']['prob'],
                      'after_prob': after['ml']['prob'], 'additional_findings': changes}))
print('Every finding retained after explicit ID and severity mapping, including archive members')
