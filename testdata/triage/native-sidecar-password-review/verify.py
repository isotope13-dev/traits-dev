"""Static controls only: no Java or native sample is executed."""
from pathlib import Path
import argparse, json, os, subprocess
p=argparse.ArgumentParser();p.add_argument('samples',type=Path);p.add_argument('scratch',type=Path);a=p.parse_args();r=a.scratch/'controls';r.mkdir(parents=True,exist_ok=True)
j=(a.samples/'14d30e64e627/PasswordHook.java').read_text();start=j.index('    void installCompat()');compat='final class PasswordHook {\n'+j[start:];(r/'compat.java').write_text(compat)
for name,old,new in [('other-method','getX.getName()','getSalt.getName()'),('other-source','event.args[0]','another.args[0]'),('other-value','Pref.applyData("password", captured)','Pref.applyData("password", unrelated)'),('other-index','event.args[0]','event.args[1]')]:
 (r/(name+'.java')).write_text(compat.replace(old,new))
method=compat[compat.index('    void installCompat()'):compat.rfind('}')]
first=method.replace('Pref.applyData("password", captured)','Pref.applyData("password", unrelated)')
second=method.replace('installCompat()', 'installOther()').replace('getX.getName()', 'getSalt.getName()')
(r/'cross-hook.java').write_text('final class MixedHooks {\n'+first+second+'}\n')
(r/'renamed.java').write_text(compat.replace('event','invocation').replace('captured','rawInput'))
(r/'utf8.java').write_text('class Text { String decode(byte[] value) { return new String(value, StandardCharsets.UTF_8); } byte[] encode(String value) { return value.getBytes(StandardCharsets.UTF_8); }}')
(r/'encode.java').write_text('class Text { byte[] encode(String value) { return value.getBytes(StandardCharsets.UTF_8); }}')
(r/'format-only.c').write_text('const char *cache = "%s/.local_data", *script = "%s.nc%lu.js", *command = "node \\\"%s\\\"";')
# Same-length substitutions preserve code layout. Changing publisher-picked names
# must not disable detection; these are derivatives, not original specimens.
binary=a.samples.parent/'extract/391941/package/addon.node';data=binary.read_bytes();assert data.count(b'.napi_cache')==1
replacement=b'.blob_cache';assert len(replacement)==len(b'.napi_cache');renamed=data.replace(b'.napi_cache',replacement).replace(b'addon.node',b'other.node').replace(b'/tmp/.%u',b'/tmp/.%d');(r/'renamed-addon.node').write_bytes(renamed)
# Retain the XOR loop but remove hidden staging. An ordinary transform is notable.
(r/'xor-only.node').write_bytes(data.replace(b'/tmp/.%u',b'/var/_%u').replace(b'%s/.napi_cache',b'%s/_napi_cache'))
cmd=['cleave','--traits-dir',str(Path.cwd()),'--format','json',str(r)]
result=subprocess.run(cmd,capture_output=True,text=True,check=True);(a.scratch/'controls.json').write_text(result.stdout);(a.scratch/'controls.log').write_text(result.stderr)
decoder=json.JSONDecoder();remaining=result.stdout;files=[]
while remaining.strip():
 obj,end=decoder.raw_decode(remaining.lstrip());files.extend(obj['files']);remaining=remaining.lstrip()[end:]
reports={Path(f['path']).name:f for f in files}
def ids(name):return {t['id']:t['crit'] for t in reports[name].get('traits',[])}
capture='objectives/credential-access/capture/input::telegram-srp-compat-password-capture';utf='micro-behaviors/data/decode/utf8::java-string-utf8-decoder';stage='objectives/anti-static/obfuscation/encoding/xor::native-node-xor-sidecar-stage';xor='micro-behaviors/data/encoding/xor::x64-vector-buffer-xor-loop'
for n in ['compat.java','renamed.java']:assert ids(n).get(capture)==5,(n,ids(n))
for n in ['cross-hook.java','other-method.java','other-source.java','other-value.java','other-index.java','utf8.java','encode.java','format-only.c']:assert not any(c==5 for c in ids(n).values()),(n,ids(n))
assert ids('utf8.java').get(utf)==3;assert utf not in ids('encode.java')
assert ids('renamed-addon.node').get(stage)==5,ids('renamed-addon.node')
assert ids('xor-only.node').get(xor)==3;assert not any(c==5 for c in ids('xor-only.node').values()),ids('xor-only.node')
print('12 controls passed: capture binding, renamed targets, UTF-8 direction, XOR/staging separation')
