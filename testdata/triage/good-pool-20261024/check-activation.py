#!/usr/bin/env python3
"""Check real fixture reachability and conservative PE near misses without executing code.
Pass the original triage inventory JSON; its files must still be locally available.
"""
import json, os, struct, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CLEAVE=os.environ.get('CLEAVE',str(ROOT.parent/'cleave/target/release/cleave'))
MARK='metadata/binary/code/control-transfer::pe-return-entry-without-callbacks'
inv=json.load(open(sys.argv[1]))
with tempfile.TemporaryDirectory(prefix='activation-controls-') as tmp:
    paths=[];expect={}
    def add(name,data,marker,minimum=0):
        p=Path(tmp)/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);paths.append(str(p));expect[str(p)]=(marker,minimum)
    source=Path(inv[69]['path']).read_bytes();nt=struct.unpack_from('<I',source,60)[0];opt=nt+24
    for i in (69,80,83):add(f'inert-{i}.exe',Path(inv[i]['path']).read_bytes(),True)
    changed=bytearray(source);changed[512]=0x90;add('changed-entry.exe',changed,False,1)
    # Existing PE fixture is PE32+. Export/TLS directories are activation surfaces.
    assert struct.unpack_from('<H',source,opt)[0]==0x20b
    for label,directory in [('exports',0),('tls',9)]:
        changed=bytearray(source);struct.pack_into('<II',changed,opt+112+directory*8,0x2000,40)
        add(label+'.exe',changed,False,1)
    workflow=b'name: Example\non: issues\njobs:\n  notify:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo "${{ github.event.issue.title }}"\n'
    add('.github/workflows/active.yml',workflow,False,1)
    add('_corpus/cases/EXAMPLE/.github/workflows/fixture.yml',workflow,False)
    add('webshell.php',b'<?php system($_REQUEST["cmd"]); ?>',False,1)
    run=subprocess.run([CLEAVE,'--traits-dir',str(ROOT),'--format','jsonl',*paths],capture_output=True,text=True,check=True)
    results={};decoder=json.JSONDecoder();rest=run.stdout.lstrip()
    while rest:
        report,n=decoder.raw_decode(rest);rest=rest[n:].lstrip()
        for f in report['files']:results[f['path']]=f['traits']
    for p,(marker,minimum) in expect.items():
        rows=results[p];ids={x['id'] for x in rows};high=[x for x in rows if x['crit']>=4]
        assert (MARK in ids)==marker,(p,ids)
        assert len(high)>=minimum,(p,high)
        if Path(p).name.startswith('inert-') or '/_corpus/' in p:assert not high,(p,high)
    print(json.dumps({'passed':len(expect),'cases':[str(Path(p).relative_to(tmp)) for p in paths]},indent=2))
