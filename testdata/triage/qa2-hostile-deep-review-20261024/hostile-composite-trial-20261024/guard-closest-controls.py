"""Reject hostile matches on the closest plausible benign artifacts.

Use neutral temporary paths so QA/test-directory suppressors cannot mask a
false positive. Pass --traits-dir to test an isolated candidate taxonomy.
"""
from pathlib import Path
import argparse,json,os,shutil,subprocess,tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
parser=argparse.ArgumentParser()
parser.add_argument('--traits-dir',type=Path,default=ROOT)
parser.add_argument('--cleave',type=Path,default=ROOT.parent/'cleave/target/release/cleave')
args=parser.parse_args()
cases=[r for r in json.loads((HERE/'cases.json').read_text()) if r['expected_class'].startswith('benign')]
assert len(cases)==6
with tempfile.TemporaryDirectory(prefix='endpoint-role-controls-') as scratch:
    paths=[];names={}
    for n,r in enumerate(cases):
        source=HERE/'controls'/r['case']/Path(r['path']).name
        target=Path(scratch)/str(n)/source.name
        target.parent.mkdir(parents=True);shutil.copyfile(source,target)
        paths.append(str(target));names[str(target)]=r['case']
    run=subprocess.run([str(args.cleave),'--traits-dir',str(args.traits_dir),'analyze','--format','jsonl',*paths],text=True,capture_output=True,env={**os.environ,'CLEAVE_SKIP_CACHE':'1'})
    assert run.returncode==0,run.stderr[-2000:]
    results=[]
    for line in run.stdout.splitlines():
        r=json.loads(line)
        if not r.get('files'):continue
        ts={t['id']:t['crit'] for f in r['files'] for t in f.get('traits',[])}
        hostile=sorted(i for i,c in ts.items() if c==5)
        results.append({'case':names[r['files'][0]['path']],'passed':not hostile,'hostile':hostile})
assert len(results)==6
print(json.dumps(results,indent=2))
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
