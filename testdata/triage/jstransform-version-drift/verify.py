"""Run focused collection/concealment controls: python3 verify.py <scratch-dir>."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CONCAT = 'micro-behaviors/data/collection/array::js-nested-index-concat'
REMAP = 'objectives/anti-static/obfuscation/string/array::js-index-remap-array-reconstruction'
SPLIT = 'metadata/lang/source/syntax/member::js-split-member-access-text'
RETIRED = {
    'objectives/anti-static/obfuscation/string/array::js-array-remap-nested-concat',
    'micro-behaviors/data/control-flow/analysis::js-nested-array-concat',
    'objectives/anti-static/obfuscation/string/fragmentation::js-split-literal-member-name',
}


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    ordinary = 'var ret = []; ret = ret.concat(handlers[order[i]]);\n'
    encoded = (
        'var chars = new Array("\\x32","\\x34");\n'
        'var order = [' + ','.join(['1', '0'] * 12) + '];\n'
        'var code = "";\n'
        'for (var i = 0; i < order.length; i++) {\n'
        '  code = code.concat(chars[order[i]]);\n'
        '}\n'
    )
    padding = '/*' + ' padding' * 2600 + ' */\n'
    cases = [
        ('ordinary.js', ordinary, {CONCAT}, {REMAP, SPLIT}),
        ('large-ordinary.js', ordinary + '/*' + ' padding' * 6500 + '*/',
         {CONCAT}, {REMAP}),
        ('single-index.js', 'var ret = []; ret = ret.concat(handlers[i]);\n',
         set(), {CONCAT, REMAP}),
        ('encoded-remap.js', encoded + 'eval(code);\n' + padding,
         {CONCAT, REMAP}, set()),
        ('encoded-without-eval.js', encoded + padding, {CONCAT}, {REMAP}),
        ('ordinary-with-eval.js', ordinary + 'eval(source);\n' + padding,
         {CONCAT}, {REMAP}),
        ('split-member.js', 'var member = target["sp"+"awn"];\n',
         {SPLIT}, set()),
        ('split-chain.js', 'var member = target["s"+"pa"+"wn"];\n',
         {SPLIT}, set()),
        ('split-member.ts', 'const member = target["sp"+"awn"];\n',
         {SPLIT}, set()),
        ('split-member.html', '<script>var member = target["sp"+"awn"];</script>\n',
         {SPLIT}, set()),
        ('comment-example.js', '// var member = target["sp"+"awn"];\n',
         {SPLIT}, set()),
        ('quoted-example.js', 'var example = \'target["sp"+"awn"]\';\n',
         {SPLIT}, set()),
        ('builtin-member.js', 'var member = Object["ke"+"ys"];\n',
         set(), {SPLIT}),
        ('variable-member.js', 'var member = target[prefix+suffix];\n',
         set(), {SPLIT}),
        ('nested-quoted-example.js', 'var member = target[\'example["sp"+"awn"]\'+suffix];\n',
         {SPLIT}, set()),
    ]
    paths = []
    for name, source, _, _ in cases:
        path = dest / name
        path.write_text(source)
        paths.append(path)
    proc = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', *map(str, paths)],
        text=True, capture_output=True, check=True)
    # Multi-target JSON output concatenates one report per target.
    decoder = json.JSONDecoder()
    remaining = proc.stdout.lstrip()
    findings = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        for f in report['files']:
            findings[f['path']] = {t['id']: t for t in f.get('traits', [])}
        remaining = remaining[end:].lstrip()
    for (name, _, required, forbidden), path in zip(cases, paths):
        traits = findings[str(path)]
        assert not required - traits.keys(), (name, 'missing', required - traits.keys())
        assert not (forbidden | RETIRED) & traits.keys(), (name, 'unexpected', traits.keys())
        if CONCAT in traits:
            assert traits[CONCAT]['crit'] == 3, (name, 'collection must be notable')
        if REMAP in traits:
            assert traits[REMAP]['crit'] == 4, (name, 'encoded remap remains suspicious')
        if SPLIT in traits:
            assert traits[SPLIT]['crit'] == 3, (name, 'source text remains notable metadata')
        print('PASS', name)


if __name__ == '__main__':
    main()
