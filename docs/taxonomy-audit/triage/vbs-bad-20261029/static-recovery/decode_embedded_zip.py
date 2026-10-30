"""Recover byte arrays into ZIP files using verified literal arithmetic only."""
from pathlib import Path
import re,json,hashlib,io,zipfile
W=Path('/tmp/vbs-bad-triage-20261029');out=[]
for folder in ['7b26eeb20bae','7bc20f7b0933','ed237ffdc804']:
 p=next((W/'extracted'/folder).glob('*.vbs'));s=p.read_text();decoded=(W/'static'/f'{folder}-array-decoded.vbs').read_text()
 const={m[1].lower():int(m[2])for m in re.finditer(r'(?im)^\s*const\s+(\w+)\s*=\s*(-?\d+)\s*$',s)}
 arr={m[1].lower():m[2]for m in re.finditer(r'(?im)^(\w+)\s*=\s*Array\(([^\n]+)\)',s)}
 match=re.search(r'(?i)For Each\s+(\w+)\s+in\s+Array\(([^\n]+)\)\s*\n\.WriteText\s+squander\((\w+)\)',decoded);assert match and match[1].lower()==match[3].lower()
 data=bytearray()
 for name in match[2].split(','):
  vals=[int(t.strip())if re.fullmatch(r'\d+',t.strip())else const[t.strip().lower()]for t in arr[name.strip().lower()].split(',')]
  units=[(x-29)%65536 for x in vals];assert all(0<=u<=255 for u in units);data.extend(units)
 assert bytes(data[:4])==b'PK\x03\x04';dst=W/'static'/f'{folder}-embedded.zip';dst.write_bytes(data)
 z=zipfile.ZipFile(io.BytesIO(data));assert len(z.infolist())<=10 and sum(i.file_size for i in z.infolist())<=32*1024*1024
 members=[]
 for i in z.infolist():
  path=Path(i.filename);assert not path.is_absolute()and '..'not in path.parts
  raw=z.read(i);sha=hashlib.sha256(raw).hexdigest();target=W/'native-payloads'/sha/Path(i.filename).name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);members.append({'name':i.filename,'size':len(raw),'sha256':sha,'path':str(target)})
 out.append({'source_archive_prefix':folder,'zip_sha256':hashlib.sha256(data).hexdigest(),'zip_size':len(data),'arrays':len(match[2].split(',')),'members':members})
(W/'embedded-zip-evidence.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
