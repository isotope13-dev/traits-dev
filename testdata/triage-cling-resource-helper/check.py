#!/usr/bin/env python3
"""Static controls. Never load or execute the samples."""
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('samples',type=Path)
p.add_argument('--cleave',default='cleave')
a=p.parse_args()
ROOT=Path(__file__).resolve().parents[2]
SAMPLES={
 'signed':('824dab563091/824dab563091954637c9d95a253ef28e41ac95e32de72b41a77fca1d26c78de8.exe','824dab563091954637c9d95a253ef28e41ac95e32de72b41a77fca1d26c78de8'),
 'cling':('3a6927a3399f/mipsel','3a6927a3399f2a10bb2e2229482e5096e5f1c3401a87f7f1730db11243531e28'),
 'helper':('a27cafb84876/a27cafb84876a3374ef4aba1062345def6cd0b029eaf8e0dc44fa24fc943f3c6.bin','a27cafb84876a3374ef4aba1062345def6cd0b029eaf8e0dc44fa24fc943f3c6')}
C2='objectives/command-and-control/channel/covert::mips-stun-transaction-task-channel'
FLOOD='objectives/impact/dos/flood::mips-stun-controlled-packet-flood'
CHACHA='micro-behaviors/crypto/symmetric/stream/chacha::mips-le-chacha-quarter-round'
WRAPPER='metadata/lang/compiler/managed::ps2exe-wrapper'
EXEC='micro-behaviors/process/create/exec::mips-o32-execve-syscall'
def scan(path):
 r=subprocess.run([a.cleave,'--traits-dir',str(ROOT),'--format','json',str(path)],capture_output=True,text=True,check=True)
 if r.stderr.strip():raise AssertionError(r.stderr)
 d=json.loads(r.stdout)
 return {t['id']:t['crit'] for f in d['files'] for t in f.get('traits',[])}
def check(name,path,yes=(),no=(),benign=False):
 ts=scan(path)
 assert all(i in ts for i in yes),(name,'missing',set(yes)-ts.keys())
 assert not (set(no)&ts.keys()),(name,'unexpected',set(no)&ts.keys())
 if benign:
  assert not any(c==5 for c in ts.values()),(name,'hostile')
  assert sum(c==4 for c in ts.values())<=1,(name,'too many suspicious')
 print('PASS',name)
with tempfile.TemporaryDirectory(prefix='.cling-trait-controls-',dir=ROOT/'testdata') as tmp:
 td=Path(tmp);data={}
 for n,(rel,sha) in SAMPLES.items():
  src=a.samples/rel;b=src.read_bytes();assert hashlib.sha256(b).hexdigest()==sha
  data[n]=b
  check(n,src,yes=[C2,FLOOD,CHACHA,EXEC] if n=='cling' else ([WRAPPER] if n=='signed' else []),benign=n!='cling')
 # This is the exact collector-renaming case that used to promote an
 # unsigned res.dll and a companion library name to hostile.
 q=td/'res.dll';q.write_bytes(data['helper']);check('renamed helper',q,no=['metadata/binary/instruction/operand::mz-words-in-code'],benign=True)
 # Altering all encryption-key bytes preserves content-independent code rules.
 b=bytearray(data['cling']);b[0x15048:0x15068]=bytes(range(32))
 q=td/'renamed-and-rekeyed.elf';q.write_bytes(b);check('renamed/rekeyed',q,[C2,FLOOD,CHACHA])
 # Remove one required role at a time; each eliminates precisely its consumers.
 for name,offset,value,yes,no in [
  ('no STUN cookie',0x3254,0x43,[CHACHA,EXEC],[C2,FLOOD]),
  ('no transaction words',0x19d4,0x14,[CHACHA,EXEC],[C2,FLOOD]),
  ('no packet send loop',0x3760,0xe9,[C2,CHACHA,EXEC],[FLOOD]),
  ('different cipher rotations',0x268d,0x35,[C2,FLOOD,EXEC],[CHACHA])]:
  b=bytearray(data['cling']);b[offset]=value;q=td/(name.replace(' ','-')+'.elf');q.write_bytes(b);check(name,q,yes,no)
 # Confirm that neutral code shape, absent the STUN leg, cannot convict.
 # Parameter fragments and ordinary consent requests are not pass-the-hash/UAC bypass.
 q=td/'settings.ps1'
 q.write_text('New-ItemProperty -Path HKCU:\\Software\\Example -Name Enabled -Value 1\nStart-Process powershell.exe -Verb RunAs\n')
 ts=scan(q)
 assert 'objectives/lateral-movement/pass-the-hash/uac::localaccount-token-filter-set' not in ts
 assert 'micro-behaviors/os/privilege/elevation::powershell-start-process-runas' in ts
 print('PASS ordinary setting and consent')
 # Perl matcher consolidation retains the text and archive-object carriers.
 for ext in ['pl','txt']:
  q=td/('shell-control.'+ext);q.write_text('exec({"/bin/sh"} ("sh", "-i"));\n')
  check('Perl shell '+ext,q,['micro-behaviors/process/create/exec::perl-exec-bin-sh'])
print('All static controls passed')
