"""Focused controls for bootstrap, callback scope, and try-block claims.

Run with --scratch pointing to a writable directory outside test paths.
Samples are analyzed statically; this check never executes their JavaScript.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).with_name('files')
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), CLEAVE_SKIP_CACHE='1',
           CLEAVE_VALIDATE='0', SCAN_NO_UPDATE='1')
movement = 'objectives/impact/ui/manipulation/harassment::browser-subsecond-random-movement'
focus = 'objectives/impact/ui/manipulation/harassment::browser-subsecond-focus-reassertion'
in_try = 'micro-behaviors/os/module/require::cjs-require-in-try'
move_code = 'window.moveTo(Math.random()*800,Math.random()*600);'
focus_code = 'window.focus();'
retired = {
    'objectives/command-and-control/backdoor/proxy/mcp::mcp-obfuscated-tokenized-detached-launch',
    'objectives/command-and-control/dropper/file-exec/detached::node-obfuscated-execpath-detached-daemon',
    'objectives/impact/degrade/resource::browser-moving-popup-lockup',
    'objectives/impact/degrade/resource::browser-interval-focus-steal',
}
cases = [
    ('mcp', (fixtures / 'mcp-backdoor-detached.js').read_text(),
     {'micro-behaviors/os/env/secret-name::javascript-credential-env-reference'}, {in_try}, 3),
    ('mcp-updater', (fixtures / 'mcp-updater-detached.js').read_text(), set(), set(), 3),
    ('popup', (fixtures / 'popup-lockup-tight.js').read_text(), {movement, focus}, set(), 4),
    ('scattered', (fixtures / 'popup-api-scattered.js').read_text(), set(), {movement, focus}, 3),
    ('nearby', move_code + focus_code + 'setInterval(function(){},100);',
     set(), {movement, focus}, 3),
    ('nested-click', 'setInterval(function(){button.onclick=function(){' +
     move_code + focus_code + '}},100);', set(), {movement, focus}, 3),
    ('slow', 'setInterval(function(){' + move_code + focus_code + '},1000);',
     set(), {movement, focus}, 3),
    ('arrow', 'setInterval(()=>{' + move_code + focus_code + '},100);',
     {movement, focus}, set(), 4),
    ('focus-only', 'setInterval(function(){' + focus_code + '},100);',
     {focus}, {movement}, 4),
    ('movement-only', 'setInterval(function(){' + move_code + '},100);',
     {movement}, {focus}, 4),
    ('require-const', "try { const x = require('optional'); } catch(e) {}",
     {in_try}, set(), None),
    ('require-var', "try { var x = require('optional'); } catch(e) {}",
     {in_try}, set(), None),
    ('require-direct', "try { require('optional'); } catch(e) {}",
     {in_try}, set(), None),
    ('require-after', "try { work(); } catch(e) {} require('optional');",
     set(), {in_try}, None),
    ('require-comment', "try { /* require('optional'); */ work(); } catch(e) {}",
     set(), {in_try}, None),
]
with tempfile.TemporaryDirectory(prefix='second-review-', dir=args.scratch) as neutral:
    for name, source, required, forbidden, ceiling in cases:
        target = Path(neutral) / (name + '.js')
        target.write_text(source)
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--format', 'json',
                                 str(target)], env=env, capture_output=True, text=True)
        assert result.returncode == 0, (name, result.stderr)
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
        assert required <= traits.keys(), (name, required - traits.keys())
        assert not (forbidden | retired) & traits.keys(), (name, (forbidden | retired) & traits.keys())
        if ceiling is not None:
            assert all(t['crit'] <= ceiling for t in traits.values()), (name, traits)
        for trait in (required & {movement, focus}):
            assert traits[trait]['crit'] == 4, (name, trait, traits[trait]['crit'])
        print('PASS', name, flush=True)
