#!/usr/bin/env python3
"""Ironheights defensive-scanner context must suppress signature self-matches.

A file carrying Ironheights identity markers (guard plugin name, pinned
advisory-key path, host denylist table, decode-pipe rule name) alongside the
`tunnel endpoint` and `decode-to-shell pipeline` strings must not report the
tunnel-domain or decode-pipe suspicious traits: those strings are signatures
the scanner detects, not behavior. The same strings without scanner context
must still convict.

Run `python3 testdata/ironheights-scanner-context/check.py <scratch-directory>`.
Fixtures are copied outside testdata so file-path suppressors cannot mask the
findings under test.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TUNNEL = ('objectives/command-and-control/infrastructure/domain/tunnel::'
          'localtunnel-me')
DECODE_PIPE = ('micro-behaviors/process/create/shell/bridge::'
               'js-decode-pipe-shell-command')
CONTEXT = ('well-known/tool/detection/ironheights::'
           'ironheights-defensive-scanner-context')
LEGS = {
    'well-known/tool/detection/ironheights::guard-plugin-name',
    'well-known/tool/detection/ironheights::pinned-advisory-key-path',
    'well-known/tool/detection/ironheights::denylist-table-marker',
    'well-known/tool/detection/ironheights::decode-pipe-rule-name',
}
expected = {
    # Scanner rule pack: legs live, both suspicious verdicts absent.
    # (The exception composite itself is never emitted.)
    'positive-scanner-rules.js': (set(), LEGS),
    # Live pipeline with no scanner context: both verdicts present.
    'negative-live-pipeline.js': ({TUNNEL, DECODE_PIPE}, set()),
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for fixture in sorted(expected):
    target = scratch / fixture
    shutil.copyfile(Path(__file__).parent / fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    suspicious = set()
    seen = set()
    for entry in report['files']:
        for trait in entry['traits']:
            if trait['crit'] == 4:
                suspicious.add(trait['id'])
            seen.add(trait['id'])
    want_suspicious, want_legs = expected[fixture]
    if want_suspicious:
        missing_verdicts = want_suspicious - suspicious
        assert not missing_verdicts, (fixture, sorted(missing_verdicts))
    else:
        assert not (suspicious & {TUNNEL, DECODE_PIPE}), \
            (fixture, sorted(suspicious & {TUNNEL, DECODE_PIPE}))
    missing = want_legs - seen
    assert not missing, (fixture, sorted(missing))
    print(f'{fixture}: passed')
