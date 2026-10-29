import json,subprocess,concurrent.futures
from pathlib import Path
base=Path('/tmp/gif-good-triage');rows=json.loads((base/'structure.json').read_text())
def run(r):
 if 'error' in r:return {'sha256':r['sha256'],'status':'invalid structure','reason':r['error']}
 p=base/'previews'/r['sha256'];p.mkdir(parents=True,exist_ok=True)
 out=subprocess.run([str(base/'decode'),r['path'],str(p),str(len(r['structure']['frames']))],capture_output=True,text=True,timeout=120)
 return {'sha256':r['sha256'],'status':'pass' if out.returncode==0 else 'failed','exit_code':out.returncode,'details':out.stdout.strip(),'stderr':out.stderr[:300],'previews':[str(x) for x in sorted(p.glob('*.ppm'))]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,rows))
(base/'independent-decode.json').write_text(json.dumps(results,indent=2)+'\n');print('decode results', {s:sum(r['status']==s for r in results) for s in set(r['status'] for r in results)})
for r in results:
 if r['status']!='pass':print(r)
