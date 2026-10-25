"""Check saved, full before/after scans; never execute specimen code.

Usage: python3 check.py <research-scratch-directory>
The directory holds atomscan before.json/after.json and cleave control reports.
"""
import collections
import json
from pathlib import Path
import sys

scratch = Path(sys.argv[1])
loader = 'objectives/anti-static/obfuscation/payload/resource::dotnet-large-base64-resource-with-assembly-resolve-loader'
vendor = 'objectives/evasion/masquerade/brand/vendor::unsigned-microsoft-vendor-claim'
identity = 'well-known/lib/runtime/managed/dotnet-runtime::dotnet-corelib-assembly'
neutral = 'metadata/signed/trust-level::unsigned-pe-microsoft-version-fields'


def reports(name):
    text = (scratch / name).read_text()
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, offset = decoder.raw_decode(text)
        yield report.get('raw', report)
        text = text[offset:]


def files(name):
    return [file for report in reports(name) for file in report['files']]


def traits(file):
    return {trait['id']: trait['crit'] for trait in file.get('traits', [])}


before = files('before.json')
after = files('after.json')
assert len(before) == len(after) == 2100
assert [f['sha'] for f in before] == [f['sha'] for f in after]
for old, new in zip(before, after):
    lost = traits(old).keys() - traits(new).keys()
    assert lost <= {loader, vendor}, (old['path'], lost)
    if vendor in lost:
        assert neutral in traits(new), new['path']
    for name, level in traits(old).items():
        if name not in {loader, vendor}:
            assert traits(new).get(name) == level, (old['path'], name)
assert collections.Counter(traits(after[0]).values())[5] == 0
assert collections.Counter(traits(after[0]).values())[4] == 1
controls = {Path(f['path']).name: traits(f) for f in files('controls.after.json')}
assert identity in controls['renamed-runtime.dll']
assert loader not in controls['renamed-runtime.dll']
assert identity not in controls['pdb-name-only.dll']
assert loader in controls['wrong-pdb.dll']
assert identity not in controls['wrong-pdb.dll']
old = traits(files('diskdiag.before.json')[0])
new = traits(files('diskdiag.after.json')[0])
assert {k: v for k, v in old.items() if v >= 4} == {k: v for k, v in new.items() if v >= 4}
assert sum(v == 5 for v in new.values()) == 2
for f in files('test-libraries.after.json'):
    assert neutral in traits(f)
    assert not any(level >= 4 for level in traits(f).values())
print('PASS: all original observations retained except the two corrected claims; controls pass')
