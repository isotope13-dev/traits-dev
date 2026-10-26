import json,sys
from pathlib import Path
p=Path(__file__).parent; inv=json.load(open(p/'inventory.json'));dec=json.JSONDecoder();text=(p/sys.argv[1]).read_text();reports=[];at=0
while at<len(text):
 while at<len(text) and text[at].isspace():at+=1
 if at==len(text):break
 try:r,at=dec.raw_decode(text,at);reports.append(r)
 except json.JSONDecodeError:break
out=[]
for i,x in enumerate(inv):
 found=[]
 for r in reports:
  raw=r.get('raw',r)
  fs=raw.get('files',[])
  if any(f.get('path')==x['path'] and f.get('sha')==x['sha256'] for f in fs):found=fs;break
 if not found:continue
 high={}
 for f in found:
  for t in f.get('traits',[]):
   if t.get('crit',0)>=4:high.setdefault(t['id'],{'crit':t['crit'],'units':[]})['units'].append(f['path'])
 out.append(dict(index=i,**x,high=high,units=len(found)))
 print(i,'H',sum(t['crit']==5 for t in high.values()),'S',sum(t['crit']==4 for t in high.values()),'units',len(found))
(p/'final-summary.json').write_text(json.dumps(out,indent=2));print('complete',len(out),'reports',len(reports))
