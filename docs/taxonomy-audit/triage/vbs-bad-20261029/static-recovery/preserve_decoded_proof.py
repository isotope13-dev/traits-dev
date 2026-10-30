from pathlib import Path
import re,json
W=Path('/tmp/vbs-bad-triage-20261029');rows=[]
for prefix in ['037fec779ea1','9c5cc8a5057a','fd18075b3f59']:
 s=(W/f'{prefix}.txt').read_text();m=re.search(r'\(\s*\(([^()]+)\)\s*\|',s);assert m
 code=''.join(chr(int(x.strip().strip("'"),16))for x in m[1].split(','));p=W/'static'/f'{prefix}-hex-program.ps1';p.write_text(code);rows.append({'source_prefix':prefix,'method':'verified literal PowerShell hexadecimal ToInt16 conversion','output':str(p),'decoded':code})
s=(W/'1586692e586f.txt').read_text();m=re.search(r'hdsjhf="([^"]+)"',s,re.I);assert m;ps=m[1][::-1];p=W/'static/1586692e586f-reversed.ps1';p.write_text(ps)
# The source explicitly reverses this character buffer before converting
# delimiter-separated hexadecimal pairs; evaluate only that fixed transform.
m=re.search(r"\$\w+='([^']{256,})'",ps,re.I);assert m
code=''.join(chr(int(x,16))for x in m[1][::-1].split('#'));p=W/'static/1586692e586f-hex-program.ps1';p.write_text(code);rows.append({'source_prefix':'1586692e586f','method':'verified character reversal then delimiter-separated hexadecimal conversion','output':str(p),'decoded':code})
(W/'hex-program-evidence.json').write_text(json.dumps(rows,indent=2)+'\n')
for x in rows:print(x['source_prefix'],repr(x['decoded'][:160]))
