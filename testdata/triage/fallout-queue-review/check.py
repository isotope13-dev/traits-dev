"""Behavioral controls: true attacks and ordinary maintenance stay distinct.
Usage: python3 check.py [--report existing-cleave-jsonl]
"""
import argparse,json,os,subprocess
from pathlib import Path
base=Path(__file__).resolve().parent
repo=base.parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path);args=ap.parse_args()
cases=json.loads((base/'cases.json').read_text())
if args.report:
    text=args.report.read_text()
else:
    run=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(repo),'--json',*[str(base/c['path']) for c in cases]],text=True,capture_output=True,check=True)
    text=run.stdout
files={}
for line in text.splitlines():
    if not line.strip():continue
    for file in json.loads(line).get('files',[]):files[Path(file['path']).resolve()]=file
for case in cases:
    file=files[(base/case['path']).resolve()]
    traits=file.get('traits',[]);ids={t['id'] for t in traits}
    assert set(case.get('required',[]))<=ids,(case['path'],'missing',set(case.get('required',[]))-ids)
    assert not set(case.get('forbidden',[]))&ids,(case['path'],'unexpected')
    for key,crit in [('hostile',5),('suspicious',4)]:
        count=sum(t['crit']==crit for t in traits)
        assert count<=case.get('max_'+key,count),(case['path'],key,count)
        assert count>=case.get('min_'+key,0),(case['path'],key,count)
print(f'{len(cases)} focused behavior controls passed')
