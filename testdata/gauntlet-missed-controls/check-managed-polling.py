"""Data-only, non-executable PE controls for the managed polling observation."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser=argparse.ArgumentParser()
parser.add_argument('--cleave',default='/home/t/src/cleave/target/release/cleave')
args=parser.parse_args()
repo=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('record_controls',repo/'testdata/managed-records-review/verify.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
loop=bytes.fromhex('17 0a 2b 31 06 28 1c 00 00 06 20 00 80 00 00 5f 16 fe 03 0b '
                  '07 2c 11 02 7b 4b 00 00 04 06 91 2d 07 02 06 28 19 00 00 06 '
                  '02 7b 4b 00 00 04 06 07 9c 06 17 58 0a 06 20 00 01 00 00 32 c7')
markers=['GetAsyncKeyState','ToUnicode','StringBuilder','Append','Keylogger']
finding='objectives/collection/keylog/polling::managed-polled-character-recording'
cases=[('polling-record-context',markers,loop,True,True),
       ('names-without-loop',markers,b'',False,False),
       ('bound-128',markers,loop.replace(bytes.fromhex('20 00 01 00 00'),bytes.fromhex('20 80 00 00 00')),False,False),
       ('wrong-high-bit',markers,loop.replace(bytes.fromhex('20 00 80 00 00'),bytes.fromhex('20 80 00 00 00')),False,False),
       ('forward-branch',markers,loop[:-1]+b'\x07',False,False),
       ('without-character-api',[s for s in markers if s!='ToUnicode'],loop,False,True),
       ('without-buffer-append',[s for s in markers if s!='Append'],loop,False,True),
       ('without-key-state',[s for s in markers if s!='GetAsyncKeyState'],loop,False,True)]
env=dict(os.environ,CLEAVE_NO_UPDATE_CHECK='1',XDG_CACHE_HOME='/tmp/gauntlet-cache',RAYON_NUM_THREADS='2')
with tempfile.TemporaryDirectory(prefix='gauntlet-polling-') as scratch:
 for name,names,code,want,want_mechanic in cases:
  path=Path(scratch)/(name+'.exe')
  path.write_bytes(module.build_pe(names,code))
  result=subprocess.run([args.cleave,'--traits-dir',str(repo),'--format=json','analyze',str(path)],
                        env=env,capture_output=True,text=True,check=True,timeout=90)
  report=json.loads(result.stdout)
  traits={t['id']:t for f in report['files'] for t in f.get('traits',[])}
  assert (finding in traits)==want,(name,'recording context')
  assert ('micro-behaviors/data/control-flow/branch::cil-high-bit-byte-limit-backedge' in traits)==want_mechanic,(name,'branch mechanic')
  assert not any(t['crit']==5 for t in traits.values()),(name,'must not convict on this evidence')
  print('PASS',name,flush=True)
