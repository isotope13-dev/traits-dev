#!/usr/bin/env python3
"""Exercise article 4078 rules; keep generated controls in cleave fixtures."""
import argparse
import base64
import json
from pathlib import Path
import re
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--artifact', type=Path, required=True, help='Recovered setup.js')
p.add_argument('--fixtures-dir', type=Path, required=True)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
root = Path(__file__).resolve().parents[3]
a.fixtures_dir.mkdir(parents=True, exist_ok=True)
source = a.artifact.read_text()
alias = 'micro-behaviors/fs/delete/file/self::unlink-const-filename-alias'
profile = 'objectives/evasion/self-delete/file/script::node-decoder-file-writer-self-removal'
family = 'well-known/malware/supply-chain/axios-hijack::axios-hijack-obfuscation'
xor = 'micro-behaviors/data/decode/xor::fromcharcode-xor-rebuild'

# Re-encode every table entry, preserving its decoded command exactly while
# changing the key, arithmetic constants, campaign token and chosen names.
table = re.search(r'stq=(\[.*?\]),ord=', source).group(1)
old_key, new_key = 'OrDeR_7077', 'Varia_9381'
def transform(text, key, factor, mask):
    return ''.join(chr(ord(c) ^ (int(key[factor*i*i % 10])
                   if key[factor*i*i % 10].isdigit() else 0) ^ mask)
                   for i, c in enumerate(text))

decoded = [transform(base64.b64decode(s[::-1].replace('_', '=')).decode(),
                     old_key, 7, 333) for s in json.loads(table)]
encoded = [base64.b64encode(transform(s, new_key, 9, 323).encode())
           .decode()[::-1].replace('=', '_') for s in decoded]
assert [transform(base64.b64decode(s[::-1].replace('_', '=')).decode(),
                  new_key, 9, 323) for s in encoded] == decoded
variant = source.replace(table, json.dumps(encoded, separators=(',', ':')))
variant = variant.replace(old_key, new_key).replace('7*r*r%10', '9*r*r%10')
variant = variant.replace('^333', '^323').replace('6202033', '8172649')
for old, new in [('stq', 'entries'), ('ord', 'secret'),
                 ('_trans_1', 'unmask'), ('_trans_2', 'unpack'), ('K', 'cleanup')]:
    variant = re.sub(r'\b' + old + r'\b', new, variant)

cases = {
    'recovered.js': (source, [alias, profile, family], []),
    'renamed.js': (variant, [alias, profile], [family]),
    'renamed.ts': (variant, [alias, profile, xor], [family]),
    'cleanup.js': ('const own = __filename; fs.unlink(own, () => {});',
                   [alias], [profile, family]),
    'cleanup.ts': ('const own = __filename; remove.rmSync(own);',
                   [alias], [profile, family]),
    'direct.js': ('const fs = require("fs"); fs.unlink(__filename, () => {});',
                  ['micro-behaviors/fs/delete/file/self::unlink-filename'], [profile]),
    'other-path.js': ('const own = __filename; fs.unlink(other, () => {});',
                      [], [alias, profile]),
    'temporary.js': ('const own = "/tmp/build-stage"; fs.unlink(own, () => {});',
                     [], [alias, profile]),
    'reassigned.js': ('let own = __filename; own = other; fs.unlink(own);',
                      [], [alias, profile]),
    'shadowed.js': ('const own = __filename; (() => { const own = other; fs.unlink(own); })();',
                    [], [alias, profile]),
    'comment.js': ('// const own = __filename; fs.unlink(own);\nconsole.log("ok");',
                   [], [alias, profile]),
    'no-remove.js': (variant.replace('t.unlink(cleanup,', 't.stat(cleanup,'),
                      [], [alias, profile]),
    'no-write.js': (variant.replace('.writeFileSync(', '.readFileSync('),
                     [alias], [profile]),
    'no-xor.js': (variant.replace('S^a^323', 'S+a+323'), [alias], [profile]),
    'no-base64.js': (variant.replace('Buffer.from(E,"base64")', 'Buffer.from(E,"utf8")'),
                      [alias], [profile]),
    'markers-only.js': ('const stq=["AAAAAAAAAAAAAAAAAAAAAAAA"];'
                        'const key="OrDeR_7077";_trans_1();', [], [family]),
    'arithmetic.js': ('const n = table[7*r*r%10];', [], [family, profile]),
}
paths = []
for name, (text, _, _) in cases.items():
    path = a.fixtures_dir / name
    path.write_text(text)
    paths.append(str(path))
# Keep controls in the engine's fixture tree, but analyze path-neutral links:
# otherwise the existing /tests/fixtures/ exception suppresses the decoder
# before the behavior under test is evaluated, including the real specimen.
with tempfile.TemporaryDirectory(prefix='rule-cases-', dir=a.artifact.parent) as scan_dir:
    scan_paths = []
    for path in paths:
        link = Path(scan_dir) / Path(path).name
        link.symlink_to(Path(path).resolve())
        scan_paths.append(str(link))
    result = subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'jsonl', *scan_paths],
                            text=True, capture_output=True, check=True)
files = {Path(f['path']).name: f for line in result.stdout.splitlines()
         for f in json.loads(line)['files']}
for name, (_, matched, missing) in cases.items():
    ids = {t['id'] for t in files[name].get('traits', [])}
    assert set(matched) <= ids, (name, 'missing', set(matched) - ids)
    assert not set(missing) & ids, (name, 'unexpected', set(missing) & ids)
print(f'{len(cases)} cases passed')
