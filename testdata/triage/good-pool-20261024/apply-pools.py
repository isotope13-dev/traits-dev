#!/usr/bin/env python3
"""Apply the reviewed manifest using hopper; default is dry-run.
Run --apply only after reviewing the static audit and passing make validate.
"""
import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
rows=json.loads((root/'audit.json').read_text())['samples']
apply='--apply' in sys.argv
results=[]
for target in ('bad','purgatory','good'):
    selected=[r for r in rows if r['target_pool']==target]
    args=['hopper','mv','-target',target]
    if not apply:args.append('-dry-run')
    args.append('-')
    run=subprocess.run(args,input='\n'.join(r['sha256'] for r in selected)+'\n',capture_output=True,text=True,timeout=300)
    result={'target':target,'samples':len(selected),'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr}
    results.append(result)
    print(target,run.returncode,run.stdout.split('Summary:')[-1].strip())
    (root/('pool-moves.json' if apply else 'pool-plan.json')).write_text(json.dumps(results,indent=2)+'\n')
    if run.returncode or ' absent' not in run.stdout or not ', 0 absent, 0 failed' in run.stdout:raise SystemExit('Pool operation needs review; see saved response.')
