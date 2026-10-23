#!/usr/bin/env python3
"""Check helper discovery and loader coverage outside test-directory exclusions."""
import argparse
import json
import lzma
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.scratch.mkdir(parents=True, exist_ok=True)
helper = 'metadata/build/compiler::stack-get-current-symbol'
loader = 'objectives/anti-static/obfuscation/eval/loader::indexed-decoder-stage-loader'
# Unchanged Emscripten canvas, WebGL, EGL and Unicode-conversion forms in both
# MuJoCo 3.16.0 and 3.17.0. These are co-occurring runtime operations.
operations = (
    'var canvasSize=dimensions(canvas);var oldWidth=canvasSize[0];var oldHeight=canvasSize[1];'
    'function uniform(location){return getUniform(program,getLocation(location));}'
    'function egl(){setError(12288);return 62006}'
    'function unicode(u0){return String.fromCharCode(u0);}'
)
cases = {
    'runtime-call.js': ('var stackSave=()=>_emscripten_stack_get_current();'
                        'var stackRestore=val=>__emscripten_stack_restore(val);', True, False),
    'runtime-declaration.js': ('function _emscripten_stack_get_current(){return sp;}'
                               'var stackRestore=val=>__emscripten_stack_restore(val);', True, False),
    'quoted-name.js': ('var doc="_emscripten_stack_get_current";'
                       'var stackRestore=val=>__emscripten_stack_restore(val);', False, True),
    'commented-name.js': ('/* _emscripten_stack_get_current */'
                          'var stackRestore=val=>__emscripten_stack_restore(val);', False, True),
}
for name, (preamble, helper_expected, loader_expected) in cases.items():
    target = args.scratch / name
    target.write_text(preamble + operations)
    debug = subprocess.run(
        [args.cleave, '--traits-dir', str(root), 'test-rules', str(target),
         '--rules', helper], check=True, capture_output=True, text=True,
    ).stdout
    observed_helper = ('\nMATCHED ' + helper + ' ') in debug
    assert observed_helper == helper_expected, (name, debug)
    output = subprocess.run(
        [args.cleave, '--traits-dir', str(root), '--format', 'json', str(target)],
        check=True, capture_output=True, text=True,
    ).stdout
    report = json.loads(output)['files'][0]
    traits = {t['id']: t['crit'] for t in report.get('traits', [])}
    assert (traits.get(loader) == 4) == loader_expected, (name, traits)
    assert traits.get('micro-behaviors/data/string/conversion::fromcharcode-call') == 3
    print('PASS', name)
# Existing real malicious fixture: retain all four concealment observations.
target = args.scratch / 'rand-user-agent.js'
target.write_bytes(lzma.decompress((root / 'testdata/hostile/rand-user-agent.js.xz').read_bytes()))
report = json.loads(subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json', str(target)],
    check=True, capture_output=True, text=True,
).stdout)['files'][0]
assert sum(t['crit'] == 4 for t in report.get('traits', [])) >= 4
assert any(t['id'].endswith('::node-capable-indexed-stage-loader') and t['crit'] == 4
           for t in report.get('traits', []))
print('PASS rand-user-agent.js (existing malicious fixture)')
