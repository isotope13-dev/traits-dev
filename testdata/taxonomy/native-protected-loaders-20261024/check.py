"""Check behavioral positives, near misses, and an optional baseline report."""
import json, os, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CASES=json.loads((HERE/'cases.json').read_text())

def reports(path):
    return {Path(f['path']).name:f for line in Path(path).read_text().split('\n')
            if line.strip() for f in json.loads(line)['files']}

if len(sys.argv)>1:
    actual=reports(sys.argv[1])
else:
    files=[str(ROOT/c['path']) for c in CASES['fixtures']]
    result=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(ROOT),'--json',*files],capture_output=True,text=True,check=True)
    actual={Path(f['path']).name:f for line in result.stdout.split('\n') if line.strip() for f in json.loads(line)['files']}
for c in CASES['fixtures']:
    f=actual[Path(c['path']).name];ids={t['id'] for t in f.get('traits',[])}
    assert set(c['matched'])<=ids,(c['case_id'],'missing',set(c['matched'])-ids)
    assert not(set(c['not_matched'])&ids),(c['case_id'],'unexpected',set(c['not_matched'])&ids)
if len(sys.argv)>2:
    before=reports(sys.argv[2]);mapping=CASES['id_map']
    for name,f in before.items():
        old={(mapping.get(t['id'],t['id']),t['crit']) for t in f.get('traits',[])}
        now={(t['id'],t['crit']) for t in actual[name].get('traits',[])}
        assert old<=now,(name,'lost coverage',old-now)
print('PASS: 10 positive/near-miss fixtures; retained mapped findings')
