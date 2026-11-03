#!/usr/bin/env python3
"""Check the variant signature alongside its obfuscation and eval evidence."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'well-known/malware/worm/vjw0rm::shuffled-vjw0rm-eval-loader'
FIRST = '%SHirstaSrgdERcP%TtteEtstlwk%/Str%aWi%lM5uieUs.AMpcivaecpitarc%ai'
SECOND = '#reOAnHWstEe%%De3t_s.gec. oepmucsdAyeO%% oSF3Ru%n%fteaeto#x%i/1lvdrnt%U%'
SHUFFLE = 'function shuffle(b){let m=[];m[z]=b.charAt(z);let t=m[x];m[x]=m[l];m[l]=t;}'
EVAL = 'eval(payload);'

def source(first=FIRST, second=SECOND, shuffle=SHUFFLE, evaluate=EVAL):
    return f'const table="{first}{second}";{shuffle}{evaluate}\n'

cases = {
    'positive': (source(), True),
    'different-first': (source(first='unrelated'), False),
    'different-interior': (source(second='unrelated'), False),
    'no-shuffle': (source(shuffle=''), False),
    'no-eval': (source(evaluate='consume(payload);'), False),
    'generic-obfuscation': (source(first='unrelated', second='unrelated'), False),
}
with tempfile.TemporaryDirectory(prefix='vjw-boundary-') as tmp:
    paths = []
    for name, (value, _) in cases.items():
        path = Path(tmp) / (name + '.js')
        path.write_text(value)
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = any(t['id'] == RULE for t in report.get('traits', []))
        assert found == cases[name][1], (name, found, cases[name][1])
print('Variant finding requires its table fragments, shuffle, and eval')
