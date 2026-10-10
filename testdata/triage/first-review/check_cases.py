"""Scan static fixtures and verify declared positive and near-miss findings."""
import argparse
import json
import subprocess
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--reports',type=Path)
args=parser.parse_args()
root=Path(__file__).resolve().parents[3]
cases=json.loads((Path(__file__).parent/'cases.json').read_text())['fixtures']
if args.reports:
    source=args.reports.read_text()
else:
    result=subprocess.run(['cleave','--traits-dir',str(root),'--format','json',*[str(root/c['path']) for c in cases]],capture_output=True,text=True,check=True,cwd=root)
    source=result.stdout
    if result.stderr.strip():
        print(result.stderr)
reports={}
decoder=json.JSONDecoder()
while source.strip():
    item,end=decoder.raw_decode(source.lstrip())
    source=source.lstrip()[end:]
    for file in item.get('files',[]):
        reports[file['path']]={trait['id'] for trait in file.get('traits',[])}
failed=[]
for case in cases:
    matches=next((v for k,v in reports.items() if k.endswith(case['path'])),None)
    if matches is None:
        failed.append({'path':case['path'],'error':'missing report'})
        continue
    missing=set(case['matched'])-matches
    unexpected=set(case['not_matched'])&matches
    if missing or unexpected:
        failed.append({'path':case['path'],'missing':sorted(missing),'unexpected':sorted(unexpected)})
print(json.dumps({'cases':len(cases),'failures':failed},indent=2))
raise SystemExit(bool(failed))
