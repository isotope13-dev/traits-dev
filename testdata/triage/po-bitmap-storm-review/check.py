"""Static controls: python3 check.py SCREENSAVER SCRATCH_DIR [CLEAVE].

Never executes the specimen. Controls isolate name/entropy from concealed PE
content and distinguish VB dispatch references from unrelated CLR references.
"""
import concurrent.futures
import json
import itertools
import re
import os
from pathlib import Path
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sample, out = map(Path, sys.argv[1:3])
engine = sys.argv[3] if len(sys.argv) > 3 else 'cleave'
out.mkdir(parents=True, exist_ok=True)
original = sample.read_bytes()
CONCEAL = 'objectives/anti-static/obfuscation/steganography/image::dotnet-bitmap-column-pe-concealment'
DISPATCH = 'objectives/execution/payload/module-load::bitmap-pe-vb-load-dispatch-references'
NAME = 'metadata/file/naming::purchase-order-number-executable-name'
RETIRED = {
    'objectives/evasion/masquerade/file/payment::purchase-order-number-exe-lure',
    'objectives/evasion/masquerade/file/payment::business-lure-high-entropy-payload',
    'objectives/evasion/masquerade/file/payment::business-lure-packed-untrusted-payload',
    'objectives/evasion/masquerade/file/payment::business-lure-large-overlay-dropper',
    'objectives/evasion/masquerade/file/payment::archive-business-lure-high-entropy-payload',
    'objectives/evasion/masquerade/file/lure::scr-named-dotnet-bitmap-pixel-reader-with-high-entropy',
    'objectives/execution/payload/module-load::bitmap-pe-vb-appdomain-dispatch',
}
# Source and declaration suffix variants feed the same observation. Preserve
# their exact match union when consolidating the naming leaf at its budget.
prefix = r'^[a-z]{2,3}([_-][A-Za-z0-9]{2,4})?'
source = re.compile(prefix + r'\.(ts|tsx)$')
declaration = re.compile(prefix + r'\.d\.(cts|mts|ts)$')
combined = re.compile(prefix + r'\.(tsx?|d\.(cts|mts|ts))$')
for stem, suffix in itertools.product(
    ['ab', 'abc', 'abcd', 'ab_AB', 'abc_aB12', 'abc_a', 'db', 'io', 'api', 'sw'],
    ['ts', 'tsx', 'd.ts', 'd.cts', 'd.mts', 'cts', 'mts', 'd.tsx', 'js', 'd.ctsx']):
    name = stem + '.' + suffix
    assert bool(source.search(name) or declaration.search(name)) == bool(combined.search(name)), name

# Locate the real column carrier by its DOS header in the first RGB column.
# Changing its BMP magic removes the validated-carrier fact, while retaining
# the program's pixel-reading and reflection API names.
magic = b'BM'
carriers = []
for offset in range(len(original) - 54):
    if original[offset:offset + 2] != magic:
        continue
    if original[offset + 14:offset + 18] != b'\x28\x00\x00\x00':
        continue
    carriers.append(offset)
assert len(carriers) == 1, carriers
bad_image = bytearray(original)
bad_image[carriers[0]:carriers[0] + 2] = b'XX'
assert original.count(b'LateCall\0') == 1
no_dispatch = original.replace(b'LateCall\0', b'OtherApi\0')
# An ordinary graphics test assembly with random inert trailing bytes is a
# control for the old name + entropy and .scr + graphics + entropy profiles.
utility = (ROOT / 'testdata/taxonomy/managed-utility-command-references/hbitmap.exe').read_bytes()
rng = random.Random(8191)
entropy_control = utility + bytes(rng.getrandbits(8) for _ in range(300000))
cases = [
    ('positive/PO #4713582.scr', original, {CONCEAL, DISPATCH, NAME}, set()),
    ('renamed/utility.exe', original, {CONCEAL, DISPATCH}, {NAME}),
    ('no-carrier/PO #4713582.scr', bytes(bad_image), {NAME}, {CONCEAL, DISPATCH}),
    ('no-dispatch/PO #4713582.scr', no_dispatch, {CONCEAL, NAME}, {DISPATCH}),
    ('name-entropy/PO #4713582.scr', entropy_control, {NAME}, {CONCEAL, DISPATCH}),
]

def run(case):
    name, content, present, absent = case
    p = out / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    env = os.environ.copy()
    env['CLEAVE_VALIDATE'] = '0'
    r = subprocess.run([engine, '--traits-dir', str(ROOT), '--format', 'json', str(p)],
                       env=env, capture_output=True, text=True, check=True)
    report = json.loads(r.stdout)
    p.with_suffix('.report.json').write_text(r.stdout)
    traits = {t['id']: t for t in report['files'][0]['traits']}
    assert present <= traits.keys(), (name, present - traits.keys())
    assert not (absent | RETIRED) & traits.keys(), (name, (absent | RETIRED) & traits.keys())
    if NAME in traits:
        assert traits[NAME]['crit'] == 3, (name, 'filename must be notable')
    if name.startswith(('name-entropy/', 'no-carrier/')):
        assert not [t['id'] for t in traits.values() if t['crit'] >= 4], name
    return {'case': name, 'result': 'pass'}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, cases))
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print('PASS: 5 static positive and near-miss controls')
