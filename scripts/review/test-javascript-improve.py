#!/usr/bin/env python3
"""Static controls for decoded transaction staging and neutral call observations."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', required=True)
    parser.add_argument('--traits-dir', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    source = (root / 'testdata/hostile/generated/javascript-good-triage/transaction-xor-stage.js').read_text()
    protected = re.compile(r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_$][\w$]*\b''')
    names = {'b', 'c', 'd', 'h', 'l', 'm', 'n', 'j', 'k', 'u', 't'}
    renamed = protected.sub(lambda m: 'local_' + m[0] if m[0] in names else m[0], source)

    def change(old, new):
        assert old in source, old
        result = source.replace(old, new)
        assert result != source
        return result

    cases = {
        'original.js': (source, True),
        'renamed.js': (renamed, True),
        'changed-address.js': (change('9BC1355344B54DEDf3E44296916eD15653844509', '0123456789abcdef0123456789abcdef01234567'), True),
        'changed-key.js': (change('$v$5;kmc$ldm*5SA', 'another-literal-XOR-key'), True),
        'different-node-program.js': (change('+d)],g)', '+unrelated)],g)'), False),
        'constant-transform-return.js': (change('return l})(atob', 'return "console.log(1)"})(atob'), False),
        'reset-accumulator.js': (change('};return l})(atob', '};l="console.log(1)";return l})(atob'), False),
        'different-input.js': (change('h["charCodeAt"](m)', 'unrelated["charCodeAt"](m)'), False),
        'addition-instead-of-xor.js': (change('))^n', '))+n'), False),
        'different-transaction-field.js': (change('["input"]["substring"]', '["value"]["substring"]'), False),
        'different-request.js': (change('https://api.binplorer.com/getTxInfo/', 'https://example.invalid/data/'), False),
        'file-argument-instead-of-eval.js': (change('["-e",', '["script.js",'), False),
        'mutable-source-binding.js': (change('try{const c=', 'try{let c='), False),
        'quoted-source.js': ('const documentation = ' + json.dumps(source) + ';', False),
        'commented-source.js': ('/* ' + source + ' */', False),
        'disjoint-quoted-chain.js': ('const documentation = ' + json.dumps(source) + ';\nfunction xor(a,b){return String.fromCharCode(a.charCodeAt(0)^b)}\nrequire("child_process").spawn("node",["-e","console.log(1)"]);', False),
    }
    call_cases = {
        'same-dot.js': ('a.push(a.shift());', True, 'dot'),
        'same-bracket.js': ('a["push"](a["shift"]());', True, 'bracket'),
        'mixed-access.js': ('a.push(a["shift"]());', True, None),
        'different-dot.js': ('a.push(b.shift());', False, 'dot'),
        'different-bracket.js': ('a["push"](b["shift"]());', False, 'bracket'),
        'quoted-call.js': ('const note = \'a["push"](a["shift"]())\';', False, 'bracket'),
        'commented-call.js': ('// a.push(a.shift());', False, None),
        'nonempty-shift.js': ('a.push(a.shift(1));', False, None),
        'same-dot.ts': ('a.push(a.shift());', True, 'dot'),
    }
    with tempfile.TemporaryDirectory(prefix='javascript-improve-') as work:
        stage = Path(work)
        for name, (body, _) in cases.items():
            (stage / name).write_text(body)
        for name, (body, _, _) in call_cases.items():
            (stage / name).write_text(body)
        result = subprocess.run([str(Path(args.cleave).resolve()), '--traits-dir', str(Path(args.traits_dir).resolve()), '--format=jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        reports = [json.loads(line) for line in result.stdout.split('\n') if line]
        files = {Path(r['files'][0]['path']).name: r['files'][0] for r in reports}
        hostile = 'objectives/command-and-control/channel/deaddrop/blockchain::transaction-xor-input-node-eval'
        bound = 'micro-behaviors/process/deploy/script-eval/input::transaction-xor-node-inline-source'
        for name, (_, positive) in cases.items():
            ids = {t['id']: t['crit'] for t in files[name].get('traits', [])}
            assert (hostile in ids) == positive, (name, ids.get(hostile), result.stderr)
            assert (bound in ids) == positive, (name, ids.get(bound))
            if positive:
                assert ids[hostile] == 5 and ids[bound] == 3
        same = 'micro-behaviors/data/collection/array::js-same-receiver-push-shift'
        for name, (_, equal, spelling) in call_cases.items():
            ids = {t['id'] for t in files[name].get('traits', [])}
            assert (same in ids) == equal, (name, ids)
            if spelling:
                assert f'micro-behaviors/data/collection/array::js-{spelling}-push-shift-call-text' in ids, (name, ids)
        print(f'JavaScript improvement regressions passed: {len(cases)} payload-flow controls, {len(call_cases)} call-relation controls; sample code not executed')


if __name__ == '__main__':
    main()
