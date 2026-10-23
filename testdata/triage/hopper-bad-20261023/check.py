#!/usr/bin/env python3
"""Focused detection boundaries; supplied samples stay outside the repository.

Run with --inventory pointing at the review's original path/hash inventory.
All samples are read as data. Neither samples nor lifecycle hooks are executed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--inventory', required=True)
p.add_argument('--atomscan', default='../scan/target/release/atomscan')
p.add_argument('--batch-payload', required=True)
p.add_argument('--output', required=True)
a = p.parse_args()
inv = json.loads(Path(a.inventory).read_text())
if isinstance(inv, dict):
    inv = inv['samples']

def sample(prefix):
    row = next(x for x in inv if x['sha256'].startswith(prefix))
    data = Path(row.get('local_path', row['path'])).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    return data

bot = 'objectives/command-and-control/remote-command/dispatch::framed-socket-tasking-download-exec'
persist = 'objectives/persistence/login/winlogon/userinit::socket-command-bot-userinit-persistence'
flood = 'objectives/impact/dos/attack/flood::socket-command-bot-randomized-http-flood'
dos = 'objectives/impact/infect/micro/appending::dos-save-entry-rewrite-and-self-append'
html = 'objectives/anti-static/obfuscation/payload/embedded::obfuscated-passworded-file-preview-smuggling'
ps = 'objectives/anti-static/obfuscation/string/conceal::powershell-strided-hidden-download-eval'
phish = 'objectives/credential-access/phishing/html-brand::ebay-suspension-public-ip-verification'
php = 'micro-behaviors/process/interpreter/eval/source::php-read-then-include-same-path'
npm = 'objectives/anti-static/obfuscation/encoding/shell::npm-postinstall-printf-command-word'
upx = 'objectives/anti-static/obfuscation/pack::upx-checksum-mismatch'
cases = []
with tempfile.TemporaryDirectory(prefix='triage-boundaries-') as tmp:
    tmp = Path(tmp)
    def add(name, data, yes=(), no=(), maxcrit=None):
        path = tmp/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        cases.append((path, set(yes), set(no), maxcrit))
    d = sample('ba6b')
    add('renamed-bot.exe', d, (bot,persist,flood))
    assert b'WinExec\x00' in d and b'Userinit\x00' in d
    add('no-exec-api.exe', d.replace(b'WinExec\x00',b'NoExec!\x00'), no=(bot,persist,flood))
    add('no-userinit.exe', d.replace(b'Userinit\x00',b'OtherKey\x00'), (bot,flood), (persist,))
    d = sample('7e080')
    add('renamed-infector.com', d, (dos,))
    needle = bytes.fromhex('b4408b9c')
    assert needle in d
    add('no-entry-write.com', d.replace(needle,bytes.fromhex('b43f8b9c'),1), no=(dos,))
    d = sample('18dce')
    add('renamed-lure.html',d,(html,))
    import re
    altered,n = re.subn(rb'(?i)document\s+password',b'Document reference',d)
    assert n
    add('no-password.html',altered,no=(html,))
    altered,n = re.subn(rb'(?i)<input\s+hidden',b'<input visible',d)
    assert n >= 3
    add('no-hidden-fields.html',altered,no=(html,))
    d = sample('cd2b')
    add('renamed-phish.html',d,(phish,))
    assert b'196.32.0.12' in d
    add('brand-domain.html',d.replace(b'196.32.0.12',b'accounts.ebay.com'),no=(phish,))
    d = Path(a.batch_payload).read_bytes()
    add('stride.bat',d,(ps,))
    altered,n = re.subn(rb'(?i)hidden',b'normal',d)
    assert n
    add('visible.bat',altered,no=(ps,))
    altered,n = re.subn(rb'\+=\s*2',b'+=1',d)
    assert n
    add('no-stride.bat',altered,no=(ps,))
    add('same-path.php','<?php function read_asset($p) { echo file_get_contents($p); require_once($p); }',(php,),maxcrit=3)
    add('different-path.php','<?php function read_asset($p,$q) { echo file_get_contents($p); require_once($q); }',no=(php,),maxcrit=3)
    add('php-comment.php','<?php /* echo file_get_contents($p); require_once($p); */',no=(php,),maxcrit=3)
    add('caller-workflow.whl',sample('96a09'),maxcrit=3)
    for version,parts in [('valid',['np','m pu','blish']),('invalid',['np',' pu','blih'])]:
        hook = 'd=$(mktemp -d); $(printf "%s%s%s $d" '+ ' '.join('"'+x+'"' for x in parts)+')'
        add(version+'/package.json',json.dumps({'name':'test-control','version':'1.0.0','scripts':{'postinstall':hook}}),(npm,))
    add('argument/package.json',json.dumps({'name':'test-control','version':'1.0.0','scripts':{'postinstall':'echo $(printf "%s%s%s" "np" "m pu" "blish")'}}),no=(npm,))
    add('checksum-one.exe',sample('3110'),(upx,))
    add('checksum-two.exe',sample('2017'),(upx,))
    # Known valid packed fixture ensures packing alone is not the new finding.
    add('valid-packed.exe',Path('../cleave/testdata/upx/activation-factory-packed.pe').read_bytes(),no=(upx,))
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(Path.cwd()))
    result = subprocess.run([a.atomscan,'--no-update','--mode','slow','--format','json','path']+[str(x[0]) for x in cases],env=env,capture_output=True,text=True)
    # Atomscan returns 1 when a hostile result is present.
    assert result.returncode in (0,1), result.stderr
    by_path = {}
    for line in result.stdout.splitlines():
        files=json.loads(line)['raw']['files']
        root=files[0]['path']
        by_path[root]={t['id']:t['crit'] for f in files for t in f.get('traits',[])}
    assert len(by_path) == len(cases), (len(by_path),len(cases),result.stderr)
    report=[]
    for path,yes,no,ceiling in cases:
        found=by_path[str(path)]
        assert yes <= found.keys(), (path.name,'missing',yes-found.keys())
        assert not no & found.keys(), (path.name,'unexpected',no & found.keys())
        if ceiling is not None:
            assert max(found.values(),default=0)<=ceiling,(path.name,{k:v for k,v in found.items() if v>ceiling})
        report.append({'case':str(path.relative_to(tmp)),'required':sorted(yes),'forbidden':sorted(no),'max_criticality':ceiling,'passed':True})
    Path(a.output).write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(report)} boundary cases passed')
