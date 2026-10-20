#!/usr/bin/env python3
"""Distinguish template construction from concatenated eval arguments."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
traits = Path(__file__).resolve().parents[3]
args.scratch.mkdir(parents=True, exist_ok=True)
depth = 'metadata/lang/javascript-features::js-ast-depth-cap-reached'
packed = 'objectives/anti-static/obfuscation/eval/loader::single-line-packed-eval-module'
evaluation = 'micro-behaviors/process/interpreter/eval/direct::js-eval-raw'
indirect = 'micro-behaviors/process/interpreter/eval/indirect::js-global-object-eval-call'
retired = 'objectives/anti-static/obfuscation/control-flow/ast::ast-depth-cap-reached-web-script'
chain = '+'.join([repr('/*' + 'x' * 128 + '*/')] * 1100)
cases = {
    'payload.js': ('eval("void 0;"+' + chain + ');\n', {depth: 3, packed: 4, evaluation: 3}, {retired}),
    'layout.js': ('document.body.innerHTML=' + chain + ';function analytics(res){eval(res)}\n', {depth: 3, evaluation: 3}, {packed, retired}),
    'multiline.js': ('document.body.innerHTML=' + chain.replace('+', '+\n') + ';\nfunction analytics(res){eval(res)}\n', {depth: 3, evaluation: 3}, {packed, retired}),
    'global.js': ('window.eval(response.text);\n', {indirect: 3}, {evaluation, packed, depth}),
    'literal.js': ('const example="window.eval(response.text)";\n', {}, {evaluation, packed, depth}),
}
for name, (content, _, _) in cases.items():
    (args.scratch / name).write_text(content)
result = subprocess.run([args.cleave, '--traits-dir', str(traits), '--format', 'json',
                         *[str(args.scratch / name) for name in cases]],
                        check=True, capture_output=True, text=True)
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
units = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    units.extend(report.get('files', [report]))
    remaining = remaining[end:].lstrip()
by_name = {Path(unit['path']).name: unit for unit in units}
for name, (_, present, absent) in cases.items():
    matches = {t['id']: t['crit'] for t in by_name[name].get('traits', [])}
    for trait, criticality in present.items():
        assert matches.get(trait) == criticality, (name, trait, matches.get(trait))
    assert not absent.intersection(matches), (name, absent.intersection(matches))
    print('PASS', name)
