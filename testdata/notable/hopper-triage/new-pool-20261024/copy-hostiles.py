"""Copy confirmed originally unflagged hostiles; verify remote SHA-256."""
import hashlib,json,shlex,subprocess
from pathlib import Path
root=Path(__file__).parent;inv=json.load(open(root/'inventory.json'));baseline=json.load(open(root/'baseline-summary.json'));indices=[13,79,94,95];receipt=[]
for i in indices:
 x=inv[i];assert x['sha256']==baseline[i]['sha256'];assert not any(v['crit']==5 for v in baseline[i]['high'].values());src=Path(x['path']);sha=hashlib.sha256(src.read_bytes()).hexdigest();assert sha==x['sha256'];dst=f'/tmp/hostile/{sha}/{src.name}';subprocess.run(['ssh','elrond','mkdir -p -- '+shlex.quote(str(Path(dst).parent))],check=True);subprocess.run(['scp','--',str(src),'elrond:'+dst],check=True);r=subprocess.run(['ssh','elrond','sha256sum -- '+shlex.quote(dst)],capture_output=True,text=True,check=True);assert r.stdout.split()[0]==sha;receipt.append({'index':i,'sha256':sha,'local':str(src),'remote':'elrond:'+dst,'verified':True});(root/'elrond-receipt.json').write_text(json.dumps(receipt,indent=2));print(i,sha,src.name,'verified')
