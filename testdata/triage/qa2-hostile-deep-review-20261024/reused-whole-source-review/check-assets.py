from pathlib import Path
import base64,configparser,hashlib,html.parser,json,re,struct,subprocess,collections
inv=json.load(open('/tmp/purgatory-reverse-review/inventory.json'));out=[]
facts={r['path']:r for r in map(json.loads,open('/tmp/purgatory-reverse-review/all-source-facts.jsonl'))}
for sample in inv:
 for m in sample['members']:
  p=Path(m['analysis_path']);data=p.read_bytes();result={'sample':sample['sha256'],'member':m['name'],'sha256':m['sha256'],'kind':m['type']}
  if m['type']=='javascript':
   assert facts[str(p)]['errors']==[];result['syntax_check']='Cleave source parser: no extraction diagnostics; module not executed'
   if m['name']=='cfg.js':
    text=data.decode();url=re.search('server_url:\\s*"([^"]+)"',text).group(1);identifier=re.search('[?&]id=([^&]+)',url).group(1)
    result.update(exported_keys=['mirror_url','server_url'],decoded_client_id=base64.b64decode(identifier).decode(),url=url,behavior='Exports a function returning URL configuration; no request is sent and no data is appended by this artifact')
  elif m['name'].endswith('.ttf'):
   assert data[:4]==b'\x00\x01\x00\x00';nt=struct.unpack_from('>H',data,4)[0];tables=[]
   for i in range(nt):
    tag,check,offset,length=struct.unpack_from('>4sIII',data,12+16*i);tag=tag.decode();assert offset+length<=len(data)
    body=bytearray(data[offset:offset+length])
    if tag=='head':body[8:12]=b'\0'*4
    body+=b'\0'*((-len(body))%4);actual=sum(struct.unpack('>'+str(len(body)//4)+'I',body))&0xffffffff;assert actual==check,(tag,hex(actual),hex(check))
    tables.append({'tag':tag,'offset':offset,'size':length,'checksum_valid':True})
   padded=data+b'\0'*((-len(data))%4);assert sum(struct.unpack('>'+str(len(padded)//4)+'I',padded))&0xffffffff==0xb1b0afba
   result.update(type='TrueType font',tables=tables,whole_font_checksum_valid=True)
  elif m['name'].endswith('template.html'):
   class Html(html.parser.HTMLParser):
    def __init__(self):super().__init__();self.scripts=[];self.current=None;self.active=[]
    def handle_starttag(self,tag,attrs):
     if tag=='script':self.current={'attrs':dict(attrs),'code':''};self.scripts.append(self.current)
     for k,v in attrs:
      if k.lower().startswith('on'):self.active.append([tag,k,v])
    def handle_endtag(self,tag):
     if tag=='script':self.current=None
    def handle_data(self,d):
     if self.current is not None:self.current['code']+=d
   h=Html();h.feed(data.decode());assert len(h.scripts)==1 and not h.active
   source=h.scripts[0]['code'].replace('__REPORT_DATA__','{}');js=Path('/tmp/purgatory-reverse-review/report-template.js');js.write_text(source)
   check=subprocess.run(['/home/t/src/cleave/target/release/cleave','facts','--format','json',str(js)],capture_output=True,text=True);assert check.returncode==0,check.stderr;assert json.loads(check.stdout)['errors']==[]
   network=re.findall(r'\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon|eval|Function)\s*\(',source);assert not network
   result.update(inline_scripts=1,remote_script_sources=[],inline_event_handlers=h.active,network_or_dynamic_code_calls=network,behavior='Renders local report data into HTML and canvas charts, including innerHTML assignments',syntax_check='passed')
  elif m['name'].endswith('.ini'):
   c=configparser.ConfigParser();c.read_string(data.decode());assert c.sections()==['exploit'];assert set(c['exploit'])=={'name','desc'}
   result.update(parsed={s:dict(c[s]) for s in c.sections()},behavior='Two declarative strings; no execution, file or network operations')
  elif m['name']=='cfg.js':
   s=data.decode();url=re.search('server_url:\\s*"([^"]+)"',s).group(1);identifier=re.search('[?&]id=([^&]+)',url).group(1);result.update(exported_keys=['mirror_url','server_url'],decoded_client_id=base64.b64decode(identifier).decode(),url=url,behavior='Exports a function returning URL configuration; no request is sent and no data is appended by this artifact')
  elif m['name'].endswith('package.json'):
   pkg=json.loads(data);result.update(entry_points={'main':pkg.get('main'),'exports':pkg.get('exports'),'bin':pkg.get('bin')},lifecycle_scripts={k:v for k,v in pkg.get('scripts',{}).items() if k in ['preinstall','install','postinstall','prepare','prepublish','prepublishOnly']},dependencies=pkg.get('dependencies',{}))
  else:result['structural_review']='Python AST/module/function inventory' if m['type']=='python' else 'Package metadata, license or resource text; reviewed as data'
  out.append(result)
Path('/tmp/purgatory-reverse-review/member-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(out),'members accounted for;',sum(m['kind']=='javascript' for m in out),'JavaScript syntax checks;',sum(m.get('whole_font_checksum_valid',False) for m in out),'font checksums verified')
