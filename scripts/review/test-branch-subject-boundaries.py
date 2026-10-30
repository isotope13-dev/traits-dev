#!/usr/bin/env python3
"""Exercise subject placement where the old branch/analysis leaves overlapped."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
CASES = {
    'set_and_membership.py': 'items = set()\nif item not in items:\n    pass\n',
    'named_loop.go': 'package example\nfunc for_loop() {}\nfunc run() { for_loop() }\n',
    'frequency.py': 'from collections import Counter\ncounts = Counter(record["action"] for record in records)\ntop = counts.most_common(1)\n',
    'early_return.py': 'def work():\n    if ready(): return\n',
    'byte_comparison.c': 'int f(void *a, void *b, void *c) { return memcmp(a,b,8)==0 || memcmp(a,c,8)==0; }\n',
    'unconditional.rb': 'while true\n  sleep(1)\nend\n',
    'named_call.js': 'function run(value) { return value.call(null); }\n',
}
with tempfile.TemporaryDirectory(prefix='branch-subject-boundaries-') as temporary:
    paths = []
    for name, source in CASES.items():
        path = Path(temporary) / name
        path.write_text(source)
        paths.append(str(path))
    output = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', 'analyze', *paths], text=True, capture_output=True, check=True)
    found = {}
    for line in output.stdout.splitlines():
        for file in json.loads(line).get('files', []):
            found[Path(file['path']).name] = {rule['id'] for rule in file.get('traits', [])}
    expected = {
        'set_and_membership.py': {'micro-behaviors/data/collection/create::set-construction', 'micro-behaviors/data/collection/membership::not-in-membership-check'},
        'named_loop.go': {'metadata/lang/source/naming/function/runtime::for-loop-symbol'},
        'frequency.py': {'micro-behaviors/data/collection/frequency::python-decision-counter', 'micro-behaviors/data/collection/frequency::python-most-common-one-call'},
        'early_return.py': {'micro-behaviors/data/control-flow/return::python-early-return-call-gate'},
        'byte_comparison.c': {'micro-behaviors/mem/compare::c-memcmp-alternative-comparisons'},
        'unconditional.rb': {'micro-behaviors/data/control-flow/loop/unconditional::source-infinite-loop-metric'},
        'named_call.js': {'micro-behaviors/data/control-flow/dispatch/named::js-function-call-method'},
    }
    for name, rules in expected.items():
        missing = rules - found[name]
        # Baseline findings without a fired consumer are intentionally stripped
        # from compact scan output. Check those predicates through the tracer.
        hidden_baselines = {
            'metadata/lang/source/naming/function/runtime::for-loop-symbol',
            'micro-behaviors/mem/compare::c-memcmp-alternative-comparisons',
            'micro-behaviors/data/control-flow/dispatch/named::js-function-call-method',
        }
        assert missing <= hidden_baselines, (name, missing, found[name])
        if missing:
            trace = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', ','.join(sorted(missing)), str(Path(temporary) / name)], text=True, capture_output=True, check=True)
            for identifier in missing:
                assert any(line.startswith('MATCHED ' + identifier + ' ') for line in trace.stdout.splitlines()), trace.stdout
            assert 'would be stripped from scan output' in trace.stdout, trace.stdout
        assert not any(rule.startswith('micro-behaviors/data/control-flow/analysis') for rule in found[name]), name
    assert not any(rule.startswith('micro-behaviors/data/control-flow/loop/') for rule in found['named_loop.go']), found['named_loop.go']
print('Branch subjects: construction, membership, names, frequencies, return, comparison and dispatch passed')
