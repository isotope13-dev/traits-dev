from pathlib import Path
import json,subprocess,os
root=Path('/home/t/src/traits-dev/testdata/triage/hopper-new-evidence-20261023');rows=json.load(open(root/'review.json'))['samples'];wanted=[x for x in rows if x['sha256'][:12] in ['6af2114b8c63','d0d3361a56e2','a58c639a1083','a5d4f63e443a','744f82adda79','58d3ffd6c841','bb9830beab57','b4fa4397c031']];paths=[x.get('relocated_local_path',x['path']) for x in wanted];out=Path('/tmp/hopper-deep-review-20261023');env={**os.environ,'CLEAVE_TRAITS_DIR':'/home/t/src/traits-dev','XDG_CACHE_HOME':'/tmp/hopper-new-review-20261023/cache'}
with (out/'final-atomscan.jsonl').open('w') as stdout,(out/'final-atomscan.log').open('w') as stderr:r=subprocess.run(['/tmp/hopper-deep-review-20261023/atomscan-final','--no-update','--follow=none','--mode','slow','--format','json','path']+paths,env=env,stdout=stdout,stderr=stderr)
assert r.returncode in [0,1,2],r.returncode
print('Scanned',len(paths),'changed original samples.')
