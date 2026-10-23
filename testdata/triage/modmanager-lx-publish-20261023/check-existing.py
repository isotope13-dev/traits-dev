"""Check retained publication and low-bit-text fixtures from earlier reviews."""
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[3]
RELEVANT={'objectives/impact/spam::install-hook-temp-manifest-and-publish','metadata/lang/source/syntax/operator::low-bit-mask-expression-text'}
cases=[]
for name in ['npm-telemetry-publish-review','google-protos-version-drift']:
    for case in json.loads((ROOT/'testdata/taxonomy'/name/'cases.json').read_text())['fixtures']:
        if RELEVANT & set(case.get('matched',[])+case.get('not_matched',[])):
            cases.append(case)
result=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(ROOT),'--format','json']+[str(ROOT/c['path']) for c in cases],capture_output=True,text=True,check=True)
# The multi-target CLI writes adjacent complete JSON reports.
remaining=result.stdout; files=[]; decoder=json.JSONDecoder()
while remaining.strip():
    remaining=remaining.lstrip();report,end=decoder.raw_decode(remaining)
    files.extend(report['files']);remaining=remaining[end:]
for case in cases:
    matched_files=[f for f in files if f['path'].endswith(case['path'])]
    assert matched_files,case['path']
    ids={t['id'] for f in matched_files for t in f.get('traits',[])}
    for field in ['matched','not_matched']:
        for tid in RELEVANT & set(case.get(field,[])):
            assert (tid in ids)==(field=='matched'),(case['path'],field,tid)
print(json.dumps({'existing_fixtures_passed':len(cases)}))
