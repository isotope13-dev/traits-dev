"""Check saved full scans, including every archive member and retained control.

Usage: python3 testdata/triage/ime-pe-arcade-20261025/check.py SCRATCH
Scans are JSON/JSONL from atomscan or concatenated JSON from cleave.
"""
import json
import pathlib
import sys

SCRATCH = pathlib.Path(sys.argv[1])
OLD_PE = 'objectives/impact/infect/binary/header::'
NEW_PE = 'micro-behaviors/fs/file/section::'
RENAMES = {
    'pe-section-append': 'pe-section-growth-edits',
    'pe-section-append-directory-strip': 'pe-section-growth-directory-clear',
    'pe-section-append-entry-hijack': 'pe-section-growth-entrypoint-edit',
    'pe-shellcode-section-entry-injection': 'pe-shellcode-section-entry-edits',
    'pe-shellcode-injection-tampers-with-mitigations': 'pe-shellcode-mitigation-edits',
    'pe-shellcode-injection-clears-certificate-table': 'pe-shellcode-certificate-directory-edits',
    'pe-shellcode-written-to-image': 'pe-shellcode-buffer-assignment',
    'pe-entry-point-redirection': 'pe-entrypoint-assignment',
}
OLD_BATCH = 'objectives/command-and-control/dropper/file-exec/command/batch::batch-powershell-irm-iex'
NEW_BATCH = 'micro-behaviors/process/deploy/script-eval::batch-powershell-irm-iex'
OLD_LONG = 'objectives/command-and-control/dropper/script-eval/response-eval/batch::batch-powershell-long-irm-iex'
NEW_LONG = 'micro-behaviors/process/deploy/script-eval::batch-powershell-long-irm-iex'
OLD_CARGO = 'objectives/supply-chain/hidden-payload/package::cargo-cdylib-loader-memory-apis'
NEW_CARGO = 'metadata/build/config::cargo-cdylib-loader-memory-features'
OLD_LSB = 'objectives/anti-static/obfuscation/steganography/lsb::png-lsb-executable-loader'
CS_LSB = 'objectives/anti-static/obfuscation/steganography/lsb::csharp-pixel-low-bit-file-execution'
PS_LSB = 'objectives/anti-static/obfuscation/steganography/lsb::powershell-pixel-low-bit-file-execution'


def objects(name):
    text = (SCRATCH / name).read_text().strip()
    decoder = json.JSONDecoder()
    while text:
        obj, size = decoder.raw_decode(text)
        yield obj
        text = text[size:].lstrip()


def files(name):
    return {f['path']: f for d in objects(name)
            for f in d.get('raw', d)['files']}


def traits(file):
    return {t['id']: t['crit'] for t in file.get('traits', [])}


def remap(id, crit):
    if id.startswith(OLD_PE):
        local = id[len(OLD_PE):]
        return (NEW_PE + RENAMES.get(local, local),
                3 if local == 'pe-section-append' else min(crit, 4))
    if id == OLD_BATCH:
        return NEW_BATCH, 3
    if id == OLD_LONG:
        return NEW_LONG, crit
    if id == OLD_CARGO:
        return NEW_CARGO, 3
    return id, crit


results = {}
for sample in ('ime', 'pe', 'arcade', 'dependency'):
    before = files(sample + ('.before.json' if sample == 'dependency' else '.baseline.json'))
    after = files(sample + '.final.json')
    assert before.keys() == after.keys(), (sample, 'file population changed')
    removed, added = [], []
    for path, old in before.items():
        b, a = traits(old), traits(after[path])
        for id, crit in b.items():
            if id == OLD_LSB:
                assert path.endswith(('candidate-test.ps1', '.tar.xz')), path
                continue  # Contrast flag mask and screenshot APIs are unrelated to code recovery.
            # The engine omits unreferenced OR wrappers. Verify their canonical
            # observations survive; no matcher or underlying capability is removed.
            if id not in a and id == 'micro-behaviors/data/arithmetic::source-low-bit-mask':
                assert a.get('metadata/lang/source/syntax/operator::low-bit-mask-expression-text') == 3
                continue
            if id not in a and id == 'micro-behaviors/ui/graphics/image::pixel-api-or-byte-conversion-references':
                assert a.get('micro-behaviors/data/encode/image/pixel::powershell-bitmap-getpixel-call') == 3
                continue
            target, level = remap(id, crit)
            assert a.get(target) == level, (sample, path, id, target, level, a.get(target))
        removed.extend((path, id, crit) for id, crit in b.items() if id not in a)
        added.extend((path, id, crit) for id, crit in a.items() if id not in b)
    # Counts on archive parents are unique traits; leaf occurrences exclude rollups.
    first = next(iter(before))
    def counts(f):
        ts = list(traits(f).values())
        return {'hostile': ts.count(5), 'suspicious': ts.count(4), 'notable': ts.count(3)}
    results[sample] = {'before': counts(before[first]), 'after': counts(after[first]),
                       'removed_occurrences': removed, 'added_occurrences': added}

# Every preexisting finding on the recovered Binject source must survive its move.
# Unrelated infection, ClickFix and embedded-image controls must retain all traits.
for stem in ('other-controls', 'stego'):
    b, a = files(stem + '.before.json'), files(stem + '.final.json')
    assert b.keys() == a.keys(), stem
    for path, f in b.items():
        actual = traits(a[path])
        for id, crit in traits(f).items():
            target, level = remap(id, crit)
            assert actual.get(target) == level, (stem, path, target, level, actual.get(target))

focused = {pathlib.Path(p).name: traits(f) for p, f in files('focused.final.json').items()}
assert focused['pixel-loader.cs'][CS_LSB] == 5
assert focused['pixel-loader.ps1'][PS_LSB] == 5
for name in ('pixel-color.cs', 'pixel-one-bit.cs', 'low-bit-codec.cs', 'pixel-different-path.cs', 'candidate-test.ps1'):
    assert not any(t in focused[name] for t in (OLD_LSB, CS_LSB, PS_LSB)), name
assert focused['installer.cmd'][NEW_BATCH] == 3
assert 5 not in focused['installer.cmd'].values()
assert focused['Cargo.toml'][NEW_CARGO] == 3
assert OLD_CARGO not in focused['Cargo.toml']
# FTP greeting execution still supplies attack admission after neutral relocation.
ftp = 'objectives/command-and-control/channel/deaddrop/ftp-banner::ftp-banner-download-execution'
baseline_controls = {pathlib.Path(p).name: traits(f) for p, f in files('focused-controls.before.json').items()}
assert baseline_controls['ftp-irm-stage.cmd'][ftp] == 5
assert focused['ftp-irm-stage.cmd'][ftp] == 5
(SCRATCH / 'comparison.json').write_text(json.dumps(results, indent=2) + '\n')
print('PASS: all sample/member findings preserved or explicitly corrected; controls retained')
for name, result in results.items():
    print(name, result['before'], '->', result['after'])
