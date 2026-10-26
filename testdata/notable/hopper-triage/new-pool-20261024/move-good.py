"""Move reviewed benign originals after hopper accepts the classifications."""
import hashlib,json,os,shutil
from pathlib import Path
root=Path(__file__).parent;rows=json.load(open(root/'audit.json'))['records'];destroot=Path('/tmp/triage/misplaced-good');destroot.mkdir(parents=True,exist_ok=True);receipt=[]
for x in rows:
 if x['target']!='good':continue
 src=Path(x['path']);expected=x['sha256'];dest=destroot/src.name
 if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()!=expected:dest=destroot/expected/src.name
 dest.parent.mkdir(parents=True,exist_ok=True)
 if src.exists():
  assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
  if not dest.exists():
   temp=dest.with_name(dest.name+'.triage-copying');shutil.copy2(src,temp);assert hashlib.sha256(temp.read_bytes()).hexdigest()==expected;os.replace(temp,dest)
  assert hashlib.sha256(dest.read_bytes()).hexdigest()==expected;src.unlink()
 assert dest.is_file() and hashlib.sha256(dest.read_bytes()).hexdigest()==expected
 receipt.append({'index':x['index'],'sha256':expected,'from':str(src),'to':str(dest),'verified':True});(root/'good-move-receipt.json').write_text(json.dumps(receipt,indent=2));print(x['index'],dest,flush=True)
assert len(receipt)==26
