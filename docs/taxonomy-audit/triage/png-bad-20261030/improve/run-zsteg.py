import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time

work=Path('/tmp/png-bad-improve/zsteg');work.mkdir(parents=True,exist_ok=True)
paths=json.loads(Path('/tmp/png-bad-triage/paths.json').read_text())
env={**os.environ,'GEM_HOME':'/tmp/png-steg-tools/gems','GEM_PATH':'/tmp/png-steg-tools/gems'}
def scan(row):
    index,path=row;start=time.monotonic()
    cmd=['/tmp/png-steg-tools/bin/zsteg','--all','--no-color','--limit','4096',path]
    try:
        r=subprocess.run(cmd,env=env,capture_output=True,timeout=180)
        stdout,stderr,code=r.stdout,r.stderr,r.returncode
    except subprocess.TimeoutExpired as e:
        stdout,stderr,code=e.stdout or b'',e.stderr or b'',124
    (work/f'{index:03d}.stdout').write_bytes(stdout)
    (work/f'{index:03d}.stderr').write_bytes(stderr)
    return dict(index=index,path=path,command=cmd,returncode=code,elapsed=round(time.monotonic()-start,2),output_bytes=len(stdout),error_bytes=len(stderr))
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for row in pool.map(scan,enumerate(paths,1)):
        rows.append(row)
        (work/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(f"{row['index']:03d}: exit={row['returncode']} {row['elapsed']}s {Path(row['path']).name}",flush=True)
