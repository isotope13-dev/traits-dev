#!/usr/bin/env python3
"""Focused coverage and placement controls; never executes a specimen."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
INFECT = 'objectives/impact/infect/binary/dos/overwrite::dos-search-truncate-self-image'
TEARDOWN = 'objectives/impact/degrade/edr/teardown::dos-overwriter-uninstalls-virus-monitor'
ROTATE = 'objectives/impact/ui/manipulation/harassment::dos-overwriter-screen-rotation'
UNINSTALL = 'objectives/impact/degrade/edr/teardown::dos-vsafe-uninstall-request'
REGEX = 'micro-behaviors/data/string/replace::powershell-base64-regex-preprocessing'
EVAL = 'objectives/anti-static/obfuscation/eval/powershell-loader::batch-fragmented-regex-base64-eval'
FRAG = 'objectives/anti-static/obfuscation/string/concat::batch-fragmented-env-loader'
MAPPING = json.loads((HERE / 'mapping.json').read_text())

def read_report(text):
    reports = []
    decoder = json.JSONDecoder()
    text = text.strip()
    while text:
        report, end = decoder.raw_decode(text)
        reports.append(report)
        text = text[end:].lstrip()
    return {'files': [f for report in reports for f in report['files']]}

def check(report):
    files = {Path(f['path']).name: f for f in report['files'] if '##' not in f['path']}
    def traits(name):
        return {t['id']: t['crit'] for t in files[name].get('traits', [])}
    a = traits('overwriter.com')
    assert all(a.get(k) == 5 for k in (INFECT, TEARDOWN, ROTATE)), a
    a = traits('fragmented-loader.cmd')
    assert a.get(FRAG) == a.get(EVAL) == 4, a
    assert a.get(REGEX) == 3, a
    assert all(k in a for k in MAPPING.values()), a
    assert not (MAPPING.keys() & a.keys()), a
    a = traits('base64-cleanup.ps1')
    assert a.get(REGEX) == 3 and EVAL not in a, a
    assert UNINSTALL not in traits('virus-monitor-query.com')
    assert not ({INFECT, TEARDOWN, ROTATE} & traits('data-file-write.com').keys())
    for name in ('linear-gotos.cmd', 'base64-data.cmd', 'echo-expansions.cmd'):
        a = traits(name)
        assert FRAG not in a and EVAL not in a, (name, a)
    a = traits('linear-gotos.cmd')
    assert a.get('metadata/lang/source/syntax/command::batch-many-short-label-gotos') == 3
    assert a.get('metadata/lang/source/syntax/command::batch-many-long-label-gotos') == 3
    assert traits('base64-data.cmd').get('metadata/lang/source/syntax/assignment::batch-many-base64-shaped-assignments') == 3
    assert traits('echo-expansions.cmd').get('metadata/lang/source/syntax/member::batch-adjacent-many-expansions') == 3
    print('PASS: malware coverage, five relocations, and six benign controls')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        check(read_report(Path(sys.argv[1]).read_text()))
    else:
        engine = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
        r = subprocess.run([engine, '--traits-dir', str(ROOT), '--format', 'json', str(HERE)], check=True, capture_output=True, text=True)
        check(read_report(r.stdout))
