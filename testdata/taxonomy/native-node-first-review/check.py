from pathlib import Path
import struct
import argparse, json, subprocess, tempfile
parser=argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args=parser.parse_args()
traits=Path(__file__).resolve().parents[3]
tmp=tempfile.TemporaryDirectory(prefix='native-node-review-')
root=Path(tmp.name)
def pe(name,text=b'\xc3',data=b'',rdata=b''):
 b=bytearray(0x800);b[:2]=b'MZ';struct.pack_into('<I',b,0x3c,0x80);b[0x80:0x84]=b'PE\0\0';struct.pack_into('<HHIIIHH',b,0x84,0x14c,3,0,0,0,0xe0,0x102)
 o=0x98;struct.pack_into('<H',b,o,0x10b);struct.pack_into('<III',b,o+16,0x1000,0x1000,0x2000);struct.pack_into('<III',b,o+28,0x400000,0x1000,0x200);struct.pack_into('<II',b,o+56,0x4000,0x200);struct.pack_into('<H',b,o+68,3);struct.pack_into('<I',b,o+92,16)
 for i,(sec,content,flags) in enumerate([(b'.text',text,0x60000020),(b'.rdata',rdata,0x40000040),(b'.data',data,0xc0000040)]):
  assert len(content)<=512
  h=o+0xe0+40*i;b[h:h+len(sec)]=sec;struct.pack_into('<IIII',b,h+8,len(content),0x1000*(i+1),0x200,0x200*(i+1));struct.pack_into('<I',b,h+36,flags);b[0x200*(i+1):0x200*(i+1)+len(content)]=content
 (root/name).write_bytes(b)
pe('modbus-framed.exe',rdata=bytes.fromhex('00 01 00 00 00 06 01 03 00 00 00 0a'))
pe('modbus-six-byte-collision.exe',rdata=bytes.fromhex('48 49 50 51 01 03 00 00 00 0a'))
pe('abe-interface-context.exe',data=bytes.fromhex('CF BE 3A 46 0D 41 7F 40 8A F5 0D F3 5A 00 5C C8'),rdata=b'app_bound_encrypted_key\0')
pe('generic-go-control-names.exe',rdata=b'main.runKeylogger\0main.doTask\0main.updTaskStatus\0main.tloop\0SELECT LogonId, StartTime, LogonType FROM Win32_LogonSession WHERE\0https://1.1.1.1/dns-query?name=\0')
strings=b'main.runKeylogger\0SetWindowsHookExW\0ToUnicodeEx\0bufio.(*Writer).WriteString\0github.com/gorilla/websocket\0'
hook=bytes.fromhex('c7 00 0d 00 00 00 8b 4c 24 24 89 48 04 c7 40 08 00 00 00 00 c7 40 0c 00 00 00 00 8b 0d 60 c3 fa 00 89 0c 24 89 44 24 04 c7 44 24 08 04 00 00 00 c7 44 24 0c 04 00 00 00 e8 00 00 00 00')
events=bytes.fromhex('81 fa 00 01 00 00 74 0c 81 fa 04 01 00 00 0f 85 00 00 00 00')
pe('keyboard-recording-profile.exe',text=hook+events,rdata=strings)
pe('keyboard-missing-event-handler.exe',text=hook,rdata=strings)
(root/'webpack.config.js').write_text('module.exports = {entry: "./app.js", output: {path: "./examples", filename: "app.js"}, module: {loaders: [{test: /\\.jsx?$/, loader: "babel-loader"}]}};')
(root/'ordinary-nested-calls.js').write_text("global['r']=require; var table=['a'];var property='0';var alias=table[property];var empty='';var other=alias;var value=other(empty,convert(source));function f(){run(3311);return 3792}")
result=subprocess.run([args.cleave, '--traits-dir',str(traits),'--disable','radare2,third-party','--format','json',str(root)],capture_output=True,text=True,check=True)
# JSON format can emit consecutive top-level reports for directory inputs.
remaining=result.stdout; decoder=json.JSONDecoder(); files=[]
while remaining.strip():
    obj,end=decoder.raw_decode(remaining.lstrip())
    files.extend(obj['files']); remaining=remaining.lstrip()[end:]
reports={Path(f['path']).name:f for f in files}
assert len(reports)==8, (len(reports),result.stderr)
def ids(name): return {t['id']:t['crit'] for t in reports[name].get('traits',[])}
modbus='micro-behaviors/communications/modbus::read-holding-registers'
keylog='objectives/collection/keylog/hook::go-keyboard-hook-recording-profile'
abe='micro-behaviors/data/config/browser-preference::app-bound-field-elevation-interface'
assert ids('modbus-framed.exe').get(modbus)==3
assert modbus not in ids('modbus-six-byte-collision.exe')
assert ids('keyboard-recording-profile.exe').get(keylog)==4
assert keylog not in ids('keyboard-missing-event-handler.exe')
assert ids('abe-interface-context.exe').get(abe)==3
for name in reports:
    assert not any(c==5 for c in ids(name).values()), (name,ids(name))
    if name!='keyboard-recording-profile.exe':
        assert not any(c==4 for c in ids(name).values()), (name,ids(name))
print('8 controls passed: framing, keyboard recording, neutral ABE and names, ordinary JS')
