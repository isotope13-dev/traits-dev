from pathlib import Path
import yaml,yara_x,json,struct,sys
root=Path(__file__).resolve().parents[3]
win=Path(sys.argv[1]).read_bytes()
dos=Path(sys.argv[2]).read_bytes()
wp=root/'micro-behaviors/communications/http/client/winhttp/native-tlv-profile.yaml'
src=yaml.safe_load(wp.read_text())['traits'][0]['if']['source']
c=yara_x.Compiler();c.add_source(src);rules=c.build()
def match(blob):return bool(yara_x.Scanner(rules).scan(blob).matching_rules)
results=[]
def test(name,blob,expected):
 actual=match(blob);results.append(dict(case=name,expected=expected,actual=actual));assert actual==expected,(name,actual)
def mutate(off,new):b=bytearray(win);b[off:off+len(new)]=new;return bytes(b)
test('original buffer flow',win,True)
test('unrelated serializer call target',mutate(0x63c56-0xc00,struct.pack('<i',0)),False)
test('HTTP body reads a different pointer local',mutate(0x60fbb-0xc00,b'\x38'),False)
test('output pointer saved to different local',mutate(0x63d3d-0xc00,b'\x38'),False)
test('secure request flag removed',mutate(0xf88d-0xc00,b'\0'),False)
# Constants/hostnames outside the matched flow must not act as identifiers.
test('unrelated PDB renamed',win.replace(b'britrad.pdb',b'renamed.pdb'),True)
benign=[]
for p in (root/'testdata/benign').rglob('*'):
 if p.is_file() and p.suffix.lower() in ['.exe','.dll','.com'] and p.stat().st_size<10000000:
  if match(p.read_bytes()):raise AssertionError('unexpected benign control '+str(p))
  benign.append(str(p.relative_to(root)))
# Native keyboard corruption atoms: test operations, not prose or filenames.
f=yaml.safe_load((root/'objectives/impact/ui/manipulation/input/dos-keyboard.yaml').read_text())['traits'][0]
c=yara_x.Compiler();c.add_source('rule keyboard { strings: $a = { '+f['if']['pattern']+' } condition: $a }');dr=c.build()
def dm(b):return bool(yara_x.Scanner(dr).scan(b).matching_rules)
for name,b,expected in [('original input corruption',dos,True),('message renamed',dos.replace(b'Claes Franzen',b'Other Message'),True),('INC CL removed',dos[:0x9e]+b'\x90\x90'+dos[0xa0:],False),('BIOS queue service replaced',dos[:0xc9]+b'\xb4\x00'+dos[0xcb:],False)]:
 actual=dm(b);results.append(dict(case=name,expected=expected,actual=actual));assert actual==expected,(name,actual)
report={'tests':results,'benign_native_controls':benign,'benign_native_control_count':len(benign)}
(root/'testdata/triage/warden-claes-review/controls.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(results),'behavior controls;',len(benign),'existing benign native fixtures')
