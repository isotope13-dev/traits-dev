"""Recover this specimen's stages offline; never expose host APIs to JavaScript.
Usage: python3 extract-stages.py <original-js> <scratch-output-directory>
Requires quickjs. This is research tooling, not a detection signature.
"""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import quickjs

source=Path(sys.argv[1]).read_text()
out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
ctx=quickjs.Context();ctx.set_memory_limit(256*1024*1024);ctx.set_time_limit(30)
try:
    ctx.eval(source)
except quickjs.JSException as exc:
    if "'WScript' is not defined" not in str(exc):raise
# The bootstrap stops at its first WScript call, but pure decoder definitions
# are available. QuickJS has no filesystem, subprocess, COM or network APIs.
fragment=source[source.index('var sinkPtr510 ='):source.index('var routeEnt151 =')]
fragment=fragment.replace('var streamItem17 = WScript[providerRef489];','var streamItem17 = "C:/Evidence/sample.js";')
ctx.eval(fragment)
ps=ctx.eval('taskTbl681');(out/'decoded.ps1').write_text(ps)
fn=source[source.index('function tableTbl366('):source.index('PacketCell94.prototype.fetch')]
ctx.eval(fn.replace('tableTbl366','decodeBytes',1).replace('return vaultItem916(f);','return f;'))
routeparts=[int(x) for x in re.search(r'\$rp=@\(([^)]+)\)',ps)[1].split(',')]
mask=int(re.search(r'\$rmm=(\d+)',ps)[1])
route=''.join(chr(x^((mask+i*7)&255)) for i,x in enumerate(routeparts))
recovered=[]
for stage,keyno,domain,suffix in [(1,5,0x44,'dll'),(2,6,0x50,'exe')]:
    encrypted=base64.b64decode(re.search(r'\$d'+str(stage)+r"=\[Convert\]::FromBase64String\('([^']+)'\)",ps)[1])
    key=[int(x) for x in re.search(r'\$k'+str(keyno)+r'=@\(([^)]+)\)',ps)[1].split(',')]
    vector=[int(x) for x in re.search(r'\$i'+str(keyno)+r'=@\(([^)]+)\)',ps)[1].split(',')]
    args=','.join(json.dumps(x) for x in [list(encrypted),key,vector,route,domain])
    decoded=bytes(json.loads(ctx.eval('JSON.stringify(decodeBytes('+args+'))')))
    image=gzip.decompress(decoded)
    assert image[:2]==b'MZ'
    path=out/f'payload{stage}.{suffix}';path.write_bytes(image)
    recovered.append({'stage':stage,'path':str(path),'size':len(image),'sha256':hashlib.sha256(image).hexdigest()})
print(json.dumps(recovered,indent=2))
