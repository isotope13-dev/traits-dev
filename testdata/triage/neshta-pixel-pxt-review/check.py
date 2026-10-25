"""Verify this review's saved scans, including genuine-binary mutations.

Usage: python3 check.py /path/to/review-fallout
The scratch reports retain original artifact hashes and provenance. Mutations
are controls for specific required legs; they are never substitute specimens.
"""
import collections
import json
import pathlib
import sys

scratch = pathlib.Path(sys.argv[1])


def documents(name):
    # Cleave emits adjacent JSON documents; source text can contain Unicode
    # line separators, so neither splitlines() nor newline framing is safe.
    source = (scratch / name).read_text()
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(source):
        while offset < len(source) and source[offset].isspace():
            offset += 1
        if offset == len(source):
            break
        value, offset = decoder.raw_decode(source, offset)
        yield value


def files(name):
    for report in documents(name):
        yield from report.get('raw', report)['files']


def traits(file):
    return {t['id']: t['crit'] for t in file.get('traits', [])}


def by_basename(name):
    return {pathlib.Path(f['path']).name: traits(f) for f in files(name)}


cs = 'objectives/anti-static/obfuscation/steganography/lsb::csharp-pixel-low-bit-file-execution'
ps = 'objectives/anti-static/obfuscation/steganography/lsb::powershell-pixel-low-bit-file-execution'
persist = 'objectives/persistence/system/registry/surface::prefix-infector-encoded-exefile-handler'
decoy = 'objectives/evasion/decoy/binary::prefix-infector-host-restoration-shell-open'
conceal = 'objectives/anti-static/obfuscation/string/runtime-decrypt::generated-xor-encoded-exefile-path'
path = 'micro-behaviors/os/registry/keys/execution::lcg-exefile-open-command-key'
restore = 'micro-behaviors/data/reassembly::x86-tail-prefix-transform-body-copy'

pixel_before = traits(next(files('pixel.before.json')))
pixel_after = traits(next(files('pixel.after.json')))
assert pixel_before[cs] == 5 and pixel_after[cs] == 4
assert pixel_before.keys() == pixel_after.keys()
assert all(pixel_after[t] == c for t, c in pixel_before.items() if t != cs)

neshta_before = traits(next(files('neshta.before.json')))
neshta_after = traits(next(files('neshta.after.json')))
assert all(neshta_after[t] == c for t, c in neshta_before.items())
assert neshta_after.keys() - neshta_before.keys() == {persist, decoy, conceal, path, restore}
assert neshta_after[persist] == neshta_after[decoy] == 5
assert neshta_after[conceal] == 4

controls_before = by_basename('pixel-controls.before.json')
controls_after = by_basename('pixel-controls.after.json')
assert controls_before.keys() == controls_after.keys()
for name, before in controls_before.items():
    after = controls_after[name]
    assert before.keys() == after.keys(), name
    for trait, criticality in before.items():
        assert after[trait] == (4 if trait == cs else criticality), (name, trait)
for name in ('pixel-loader.cs', 'pixel-qualified.cs'):
    assert controls_after[name][cs] == 4
for name in ('pixel-color.cs', 'pixel-one-bit.cs', 'low-bit-codec.cs', 'pixel-different-path.cs'):
    assert cs not in controls_after[name]
assert controls_after['pixel-loader.ps1'][ps] == 5

native = by_basename('native-controls.after.json')
native_trait = 'objectives/anti-static/obfuscation/steganography/lsb::batch-python-image-low-bit-native-payload'
assert native['image-native-positive.bat'][native_trait] == 5
assert native_trait not in native['image-data-only.bat']
assert native_trait not in native['native-buffer-no-image.bat']

mutations = by_basename('mutations.after.jsonl')
assert persist not in mutations['no-encoded-handler.exe']
assert conceal not in mutations['no-encoded-handler.exe']
assert mutations['no-encoded-handler.exe'][decoy] == 5
assert decoy not in mutations['no-host-reassembly.exe']
assert mutations['no-host-reassembly.exe'][persist] == 5
assert persist not in mutations['no-registry-setter.exe']
for name in ('no-prefix-infector.exe', 'data-and-imports-only.exe', 'restored-host.exe'):
    assert persist not in mutations[name] and decoy not in mutations[name], name
assert all(c < 4 for c in mutations['restored-host.exe'].values())

# Every local archive unit and trait is identical, including decoded members.
def observation_counts(name):
    return collections.Counter(
        (f['path'], f.get('sha'), t['id'], t['crit'])
        for f in files(name) for t in f.get('traits', []))

assert observation_counts('pxt.local.before.json') == observation_counts('pxt.local.after.json')
before = observation_counts('pxt.before.json')
after = observation_counts('pxt.after.json')
# Registry feed timestamps can change; all stable-byte observations must stay.
stable_paths = {f['path'] for f in files('pxt.before.json') if not f['path'].endswith('.registry.json')}
lost = {key: n - after[key] for key, n in before.items()
        if key[0] in stable_paths and n > after[key]}
assert not lost, lost

deps_before = by_basename('dependencies.before.jsonl')
deps_after = by_basename('dependencies.after.jsonl')
assert deps_before == deps_after
assert all(c < 4 for ts in deps_after.values() for c in ts.values())
print('PASS: original coverage retained; severity corrected; new attack legs required; archive/dependencies preserved')
