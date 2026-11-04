#!/usr/bin/env python3
"""Check destructive route and neutral HTTP trigger evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
assert not (repo / 'objectives/command-and-control/trigger/http').exists()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
source = '''const root = path.join(process.cwd(), "src");
app.get("/robots.txt", (req, res) => { if (req.query.verify === "destroy") selfDestruct(); });
function selfDestruct() { fs.rmSync(root, {recursive: true}); }
'''
with tempfile.TemporaryDirectory(prefix='http-activation-') as tmp:
    root = Path(tmp)
    cases = {
        'kotlin.kt': 'val a="/trigger"; val b="/commands"; if (now.hour !in 2..5) run()\n',
        'kotlin_no_gate.kt': 'val a="/trigger"; val b="/commands";\n',
        'perl.pl': 'my $a="/trigger/check?id="; my $b="TRIGGER_FIRED"; my $c="/trigger/result"; my $cmd = $1; my $r=`$cmd 2>&1`;\n',
        'perl_no_exec.pl': 'my $a="/trigger/check?id="; my $b="TRIGGER_FIRED"; my $c="/trigger/result";\n',
        'wipe.js': source,
        'no_wipe.js': source.replace('recursive: true', 'recursive: false'),
        'trigger.cs': 'class A { string endpoint = "https://example.com/trigger"; string v = "execute activate"; }\n',
        'endpoint.cs': 'class A { string endpoint = "https://example.com/trigger"; }\n',
        'env.js': 'if (process.env["REGION"] === "RU") run();\n',
    }
    for name, text in cases.items():
        (root / name).write_text(text)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    kotlin = 'objectives/execution/trigger/network::kotlin-route-hour-window-clues'
    perl = 'objectives/command-and-control/remote-command/shell::perl-triggered-command-c2'
    assert kotlin in ids['kotlin.kt'], ids['kotlin.kt']
    assert kotlin not in ids['kotlin_no_gate.kt']
    assert perl in ids['perl.pl'], ids['perl.pl']
    assert perl not in ids['perl_no_exec.pl']
    wipe = 'objectives/impact/wipe/directory::express-robots-destroy-trigger'
    profile = 'objectives/execution/trigger/network::dotnet-http-trigger-activation'
    env = 'micro-behaviors/os/env/test::env-check-js--rx-2'
    assert wipe in ids['wipe.js'], ids['wipe.js']
    assert wipe not in ids['no_wipe.js']
    assert profile in ids['trigger.cs'], ids['trigger.cs']
    assert profile not in ids['endpoint.cs']
    assert env in ids['env.js'], ids['env.js']
    print('Destructive routes, endpoint clues and environment comparisons stay distinct.')
