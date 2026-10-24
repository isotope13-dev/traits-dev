#!/usr/bin/env python3
"""Static source/PE controls; no specimen or generated executable is run."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import io
from pathlib import Path
import re
import struct
import subprocess
import pefile
import dnfile
import olefile
from asn1crypto import cms

ap = argparse.ArgumentParser()
ap.add_argument('--paths', type=Path, required=True)
ap.add_argument('--output', type=Path, required=True)
ap.add_argument('--baseline', type=Path, required=True)
ap.add_argument('--cleave', default='cleave')
ap.add_argument('--only', help='Run control names containing this substring')
a = ap.parse_args()
a.output.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
paths = json.loads(a.paths.read_text())
R = 'objectives/impact/degrade/system/recovery::node-silent-boot-recovery-sabotage'
H = 'objectives/evasion/process/concealment::screenconnect-installer-hidden-unattended-access'
OLD_H = 'objectives/evasion/process/concealment::screenconnect-msi-hidden-unattended-access'
N = 'micro-behaviors/process/interpreter/runtime/clr::signed-embedded-pe-resolution-api-profile'
OLD_N = 'objectives/anti-static/obfuscation/binary-metrics/profile::signer-evidenced-embedded-pe-api-resolution'
C = 'micro-behaviors/process/create/exec::embedded-pe-process-as-user-profile'
OLD_C = 'objectives/command-and-control/dropper/staging/resource::signed-multistage-resource-carrier'
O = 'metadata/binary/resource/embedded-media::ole2-compound-header'
OLD_O = 'objectives/command-and-control/dropper/file-exec/spawn::ahk-embedded-ole2'
S = 'metadata/package/files/msi::service-exe-wrapper-name-reference'
OLD_S = 'objectives/persistence/system/service/install::msi-service-wrapper-binaries'
J = 'micro-behaviors/time/schedule/interval::jphp-autostart-archive-url'
OLD_J = 'micro-behaviors/process/create/exec::jphp-autostart-zip-downloader'
AHK = 'objectives/command-and-control/dropper/file-exec/spawn::autohotkey-embedded-compound-dropper'
controls = []

def add(name, content, present=(), absent=(), old_present=(), old_absent=()):
    p = a.output/name
    p.write_bytes(content.encode() if isinstance(content,str) else content)
    controls.append((p,set(present),set(absent),set(old_present),set(old_absent)))

source = Path(paths['t']).read_text()
add('recovery-renamed.js', source.replace('execSync}', 'execSync: run}').replace('execSync(', 'run('), [R])
for name,old,new in [
    ('enabled', 'recoveryenabled No', 'recoveryenabled Yes'),
    ('visible', "stdio:'ignore'", "stdio:'inherit'"),
    ('logged', 'catch(e){}', 'catch(e){console.error(e)}'),
    ('unbound', 'execSync(', 'other('),
    ('parameterized', 'function()', 'function(options)'),
    ('benign-policy', 'ignoreallfailures', 'displayallfailures'),
]:
    add('recovery-'+name+'.js', source.replace(old,new), absent=[R])

b = Path(paths['pe']).read_bytes()
add('original-wrapper.exe', b, [H,N,O,S], [OLD_N,OLD_O,OLD_S],
    [OLD_N,OLD_O,OLD_S], [OLD_H])
notice = rb'(<setting name="AccessShow(?:BalloonOnConnect|BalloonOnHide|SystemTrayIcon)"[^<]+<value>)false(</value>)'
visible,count = re.subn(notice, rb'\g<1>true \2', b)
assert count == 3
add('visible-wrapper.exe', visible, [N,O,S], [H], [OLD_N,OLD_O,OLD_S], [OLD_H])
one_visible,count = re.subn(notice, rb'\g<1>true \2', b, count=1)
assert count == 1
add('one-visible-wrapper.exe', one_visible, [H,N])
assert b'?e=Access&y=Guest&' in b
add('non-access-wrapper.exe', b.replace(b'?e=Access&y=Guest&',b'?e=Manual&y=Guest&'), [N], [H])
# A same-width import-table mutation exercises the complete old carrier
# predicate without inventing an executed malicious stage.
pe = pefile.PE(data=b)
imp = pe.DIRECTORY_ENTRY_IMPORT[1].imports[0]
mut = bytearray(b)
name_offset = pe.DIRECTORY_ENTRY_DEBUG[0].struct.PointerToRawData + 24
symbol = b'\0\0CreateProcessAsUserW\0'
mut[name_offset:name_offset+len(symbol)] = symbol
for rva in [imp.thunk_rva, imp.address-pe.OPTIONAL_HEADER.ImageBase]:
    struct.pack_into('<I',mut,pe.get_offset_from_rva(rva),pe.get_rva_from_offset(name_offset))
certificate = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4]
signed_data = cms.ContentInfo.load(b[certificate.VirtualAddress+8:
                                   certificate.VirtualAddress+certificate.Size])
signature = signed_data['content']['signer_infos'][0]['signature'].native
signature_offset = b.index(signature, certificate.VirtualAddress)
mut[signature_offset] ^= 1
add('api-profile-import-control.exe',bytes(mut),[C],[OLD_C],[OLD_C])
add('no-compound-header.exe',b.replace(bytes.fromhex('d0cf11e0a1b11ae1'),b'NOTOLE!!'),absent=[O],old_absent=[OLD_O])
add('no-wrapper-name.exe',b.replace(b'ServiceExeWithService',b'X'*21).replace(b'ServiceExeWithoutService',b'X'*24),absent=[S],old_absent=[OLD_S])
# XML boundaries are tested both in PE unsigned attributes and as standalone
# source; line-oriented extraction must not lose a split name/value relation.
config_flag = b'<setting name="AccessShowUnderControlBanner"'
config_pos = b.index(config_flag)
config_start = b.rfind(b'<?xml', 0, config_pos)
config_end = b.index(b'</configuration>', config_pos) + len(b'</configuration>')
xml = b[config_start:config_end]
for name,content in [('prefixed',xml),('unprefixed',xml.replace(b'AccessShow',b'Show'))]:
    add(name+'.xml',content,['well-known/dual-use/remote-admin/screenconnect::msi-stealth-access-group'])
# Retain the old text matcher's UTF-16LE surface as well as ASCII multiline.
wide_config = b'<ScreenConnect.ApplicationSettings>'
for flag in [b'ShowBalloonOnConnect', b'ShowBalloonOnHide', b'ShowSystemTrayIcon']:
    wide_config += b'<setting name="'+flag+b'"><value>false</value></setting>'
wide_pe = bytearray(b)
wide_data = wide_config.decode().encode('utf-16le')
wide_pe[0x550000:0x550000+len(wide_data)] = wide_data
add('wide-settings.exe',bytes(wide_pe),
    ['well-known/dual-use/remote-admin/screenconnect::msi-stealth-access-group'],
    old_present=['well-known/dual-use/remote-admin/screenconnect::msi-stealth-access-group'])
entry = next(item for group in pe.DIRECTORY_ENTRY_RESOURCE.entries
             if str(group.name) == 'FILES'
             for item in group.directory.entries if str(item.name) == '_ENTRYPOINT')
resource = entry.directory.entries[0].data.struct
entry_pe = dnfile.dnPE(data=pe.get_data(resource.OffsetToData, resource.Size))
msi = next(resource.data for resource in entry_pe.net.resources
           if str(resource.name).endswith('.ClientSetup.msi'))
line = b'<configuration><ScreenConnect.ApplicationSettings><setting name="ClientLaunchParameters"><value>?e=Access&amp;y=Guest</value></setting>'
for name in [b'ShowBalloonOnConnect',b'ShowBalloonOnHide',b'ShowSystemTrayIcon']:
    line += b'<setting name="'+name+b'" serializeAs="String"><value>false</value></setting>'
line += b'</ScreenConnect.ApplicationSettings></configuration>'
# Put the legacy one-line configuration in a real uncompressed CAB member.
# Appending arbitrary text to an MSI is not equivalent to its parsed members.
filename = b'app.config\0'
data_offset = 36+8+16+len(filename)
cab_size = data_offset+8+len(line)
cab = struct.pack('<4sIIIIIBBHHHHH', b'MSCF',0,cab_size,0,44,0,3,1,1,1,0,0,0)
cab += struct.pack('<IHH',data_offset,1,0)
cab += struct.pack('<IIHHHH',len(line),0,0,0,0,0)+filename
cab += struct.pack('<IHH',0,len(line),len(line))+line
msi_stream = io.BytesIO(msi)
with olefile.OleFileIO(msi_stream, write_mode=True) as compound:
    cabinets = [name for name in compound.listdir()
                if compound.openstream(name).read(4)==b'MSCF']
    assert len(cabinets)==1
    size = compound.get_size(cabinets[0])
    assert len(cab)<=size
    compound.write_stream(cabinets[0],cab.ljust(size,b'\0'))
add('legacy-hidden.msi',msi_stream.getvalue(),[H],old_present=[OLD_H])

jphp = '<?php /* @event timer.action */ $timer->autoStart = true; $url="https://example.org/application.zip";'
add('ordinary-timer.php',jphp,[J],[OLD_J],old_present=[OLD_J])
add('timer-no-archive.php',jphp.replace('.zip','.json'),absent=[J],old_absent=[OLD_J])
add('timer-disabled.php',jphp.replace('autoStart = true','autoStart = false'),absent=[J],old_absent=[OLD_J])

def inert_pe(parts):
    # A RET entry; data sections are unexecuted matcher controls.
    data=bytearray(512+512*len(parts))
    data[:2]=b'MZ';struct.pack_into('<I',data,0x3c,0x80)
    data[0x80:0x84]=b'PE\0\0';struct.pack_into('<HHIIIHH',data,0x84,0x14c,len(parts),0,0,0,224,0x102)
    o=0x98;struct.pack_into('<H',data,o,0x10b)
    for offset,value in {4:512,16:4096,20:4096,28:0x400000,32:4096,36:512,56:(len(parts)+1)*4096,60:512,92:16}.items():
        struct.pack_into('<I',data,o+offset,value)
    struct.pack_into('<H',data,o+68,2)
    for i,(name,content) in enumerate(parts):
        assert len(content)<=512
        sec=o+224+i*40;data[sec:sec+8]=name.encode().ljust(8,b'\0')
        struct.pack_into('<IIII',data,sec+8,512,(i+1)*4096,512,512+i*512)
        struct.pack_into('<I',data,sec+36,0x60000020 if i==0 else 0x40000040)
        data[512+i*512:512+i*512+len(content)]=content
    return bytes(data)
script=b'AutoHotkey v1.1.36.02\0FileInstall, agent.msi, C:\\Temp\\agent.msi, 1\nRun, C:\\Temp\\agent.msi\n'
for name,scr,ole,want in [
    ('ahk-payload',script,bytes.fromhex('d0cf11e0a1b11ae1'),True),
    ('ahk-no-compound',script,b'ordinary data',False),
    ('ahk-no-run',script.replace(b'Run,',b'Log,'),bytes.fromhex('d0cf11e0a1b11ae1'),False),
]:
    add(name+'.exe',inert_pe([('.text',b'\xc3'),('.rdata',scr),('.rsrc',ole)])+b'\0'*100000,
        [AHK] if want else [], [] if want else [AHK],
        [AHK] if want else [], [] if want else [AHK])

renames={OLD_N:N,OLD_C:C,OLD_O:O,OLD_S:S,OLD_J:J,OLD_H:H}
def scan(case):
    p,required,forbidden,old_required,old_forbidden=case
    result={'case':p.name}
    for label,traits,req,no in [('after',root,required,forbidden),('before',a.baseline,old_required,old_forbidden)]:
        cp=subprocess.run([a.cleave,'--traits-dir',str(traits),'--format','json',str(p)],text=True,capture_output=True)
        assert cp.returncode in (0,1),(p.name,label,cp.stderr)
        diagnostics = cp.stderr.splitlines()
        # Broad third-party YARA scans can log wall time during concurrent MSI
        # member analysis. Retain those diagnostics; rule/load warnings fail.
        assert all('Slow YARA scan before trait evaluation' in line
                   for line in diagnostics),(p.name,label,cp.stderr)
        d=json.loads(cp.stdout)
        (a.output/(p.name+'.'+label+'.json')).write_text(cp.stdout)
        ids={t['id'] for f in d['files'] for t in f.get('traits',[])}
        assert req<=ids,(p.name,label,'missing',sorted(req-ids))
        assert not no&ids,(p.name,label,'unexpected',sorted(no&ids))
        result[label]={'hostile':sorted(t['id'] for f in d['files'] for t in f.get('traits',[]) if t['crit']==5),
                       'diagnostics':diagnostics}
    return result
if a.only:
    controls = [control for control in controls if a.only in control[0].name]
with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(scan,controls))
(a.output.parent/'control-results.json').write_text(json.dumps(results,indent=2))
print(f'{len(results)} static controls passed, each scanned before and after')
