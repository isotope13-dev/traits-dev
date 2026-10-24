from pathlib import Path
import json,hashlib,subprocess,os,struct,zlib,pefile
r=Path('/tmp/hopper-new-review-20261023');out=Path('/tmp/hopper-deep-review-20261023/packing-controls');out.mkdir(exist_ok=True);inv=json.load(open(r/'inventory.json'));cases=[]
def blob(sha):return Path(next(x['path'] for x in inv if x['sha256'].startswith(sha))).read_bytes()
def add(name,b,required=(),forbidden=()):
 p=out/(name+'.exe');p.write_bytes(b);cases.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'required':list(required),'forbidden':list(forbidden)})
pack='objectives/anti-static/pack/upx::writable-upx-with-substantial-opaque-overlay';integrity='metadata/binary/layout/compression::upx-checksum-mismatch';recovery='metadata/binary/layout/compression::upx-checksum-repaired-analysis-copy';clr='objectives/anti-static/obfuscation/payload/resource::native-table-decoded-clr-resource';go='objectives/anti-static/obfuscation/encoding/arithmetic::self-issued-garbled-go-native-dispatch';trailer='objectives/anti-static/obfuscation/payload/encrypted::garbled-go-stack-strings-opaque-trailer'
fixture=Path('/home/t/src/traits-dev/testdata/taxonomy/pe-upx-section-layout-controls/near-miss-no-upx-label.exe').read_bytes();fake=bytearray(fixture);fake[64:68]=b'UPX!';add('invalid-upx-marker-image',fake,required=['metadata/binary/layout/compression::upx-invalid-packed-image'],forbidden=[recovery])
b=blob('b4fa4397c031');add('renamed-corrupt-upx',b,[pack,integrity,recovery]);add('upx-without-overlay',b[:84992],forbidden=[pack]);add('upx-zero-overlay',b[:84992]+bytes(len(b)-84992),forbidden=[pack]);d=pefile.PE(data=b);ss=d.sections[1];bb=bytearray(b);struct.pack_into('<I',bb,ss.get_file_offset()+36,ss.Characteristics&~0x80000000);add('upx-readonly-entry',bb,forbidden=[pack]);at=b.index(b'UPX!');bb=bytearray(b);clen=struct.unpack_from('<I',bb,at+20)[0];plain=Path('/tmp/hopper-deep-review-20261023/upx-raw-decoded.bin').read_bytes();struct.pack_into('<II',bb,at+8,zlib.adler32(plain),zlib.adler32(bb[at+32:at+32+clen]));bb[at+31]=sum(bb[at+4:at+31])%251;add('valid-upx-analysis-copy',bb,forbidden=[integrity,recovery])
for sha in ['58d3ffd6c841','bb9830beab57']:
 b=blob(sha);add('renamed-clr-'+sha,b,[clr]);pattern=bytes.fromhex('0fb614300fb65c300181c200010000');assert pattern in b;add('no-table-decoder-'+sha,b.replace(pattern,bytes([0x90])*len(pattern)),forbidden=[clr])
for sha in ['a58c639a1083','a5d4f63e443a','744f82adda79']:
 b=blob(sha);d=pefile.PE(data=b);sec=d.OPTIONAL_HEADER.DATA_DIRECTORY[4];bb=bytearray(b);struct.pack_into('<II',bb,sec.get_file_offset(),0,0);add('no-self-issued-cert-'+sha,bb,forbidden=[go])
b=blob('d0d3361a56e2');add('no-encrypted-trailer-go',b[:15967232],forbidden=[trailer])
env={**os.environ,'XDG_CACHE_HOME':str(r/'cache')};cmd=[os.environ.get('CLEAVE_FINAL','/home/t/src/cleave/target/release/cleave'),'--no-update-check','--traits-dir','/home/t/src/traits-dev','--disable','radare2','analyze','--format','json']+[c['path'] for c in cases];rr=subprocess.run(cmd,stdout=(out/'scan.json').open('w'),stderr=(out/'scan.log').open('w'),env=env);assert rr.returncode==0;ss=(out/'scan.json').read_text().lstrip();dec=json.JSONDecoder();files={}
while ss:
 d,n=dec.raw_decode(ss);ss=ss[n:].lstrip();files.update({f['path']:f for f in d['files']})
for c in cases:
 f=files[c['path']];ids={t['id'] for t in f['traits']};c['failures']=['missing '+x for x in c['required'] if x not in ids]+['unexpected '+x for x in c['forbidden'] if x in ids];c['high']=[{k:t[k] for k in ['id','crit','desc']} for t in f['traits'] if t.get('crit',0)>=4]
 # Recovered bytes must equal the independently unpacked analysis copy.
 if c['path'].endswith('/renamed-corrupt-upx.exe'):
  children=[v for p,v in files.items() if p.startswith(c['path']+'!!upx@')];expected=hashlib.sha256(Path('/tmp/hopper-deep-review-20261023/upx-recovered-raw-1.exe').read_bytes()).hexdigest();c['recovered_child_hash_matches']=any(v.get('sha')==expected for v in children)
  if not c['recovered_child_hash_matches']:c['failures'].append('UPX child hash does not match independent unpacking')
result={'passed':sum(not c['failures'] for c in cases),'failed':sum(bool(c['failures']) for c in cases),'cases':cases};(out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));raise SystemExit(bool(result['failed']))
