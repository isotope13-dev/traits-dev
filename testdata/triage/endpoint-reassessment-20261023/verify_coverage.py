#!/usr/bin/env python3
"""Verify that every endpoint-judgment clause is an emitted cleave finding."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--report',type=Path,default=Path(__file__).with_name('review.json'))
p.add_argument('--scan-json',type=Path,help='Fresh atomscan JSONL, otherwise rescan all samples')
p.add_argument('--atomscan',default='../scan/target/release/atomscan')
a=p.parse_args()
report=json.loads(a.report.read_text())
coverage=json.loads(a.report.with_name('cleave-coverage.json').read_text())
if a.scan_json:
    lines=a.scan_json.read_text().splitlines()
else:
    proc=subprocess.run([a.atomscan,'--no-update','--mode','slow','--format','json','path']+
        [s['local_path'] for s in report['samples']],capture_output=True,text=True,
        env=dict(os.environ,CLEAVE_TRAITS_DIR=str(Path.cwd())))
    assert proc.returncode in (0,1,2),proc.stderr
    lines=proc.stdout.splitlines()
scan={}
for line in lines:
    files=json.loads(line)['raw']['files']
    scan[files[0]['sha']]=files
assert len(scan)==len(report['samples'])==len(coverage['samples'])==25
recorded={s['sha256']:s for s in coverage['samples']}
clauses=0
for sample in report['samples']:
    sha=sample['sha256'];row=recorded[sha];files=scan[sha]
    assert hashlib.sha256(Path(sample['local_path']).read_bytes()).hexdigest()==sha
    assert row['target']==sample['target']
    assert row['claims']==sample['cleave_evidence']
    descriptions=[]
    for claim in row['claims']:
        hits=[(f,t) for f in files for t in f.get('traits',[]) if t['id']==claim['trait_id']]
        assert hits,(sample['name'],claim['trait_id'])
        assert all(t['desc']==claim['description'] and t['crit']==claim['criticality'] for f,t in hits)
        emitted={(f['path'],f['sha']) for f,t in hits}
        assert all((m['source'],m['sha256']) in emitted for m in claim['matches'])
        descriptions.append(claim['description']);clauses+=1
    expected=sample['target'].capitalize()+': '+'; '.join(descriptions)+'.'
    assert sample['endpoint_judgment']==row['endpoint_judgment']==expected
    assert 'analyst_reverse_engineering_observations' in sample
print(f'{len(scan)} endpoint judgments and {clauses} behavior clauses verified against cleave output')
