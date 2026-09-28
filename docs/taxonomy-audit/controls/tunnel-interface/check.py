"""Scan source/configuration and inert PE controls, never execute them.

Use --before to capture the original IDs; otherwise compare mapped verdicts
with the checked-in pre-migration baseline. PE fixtures need clang and lld-link.
"""
import argparse
import concurrent.futures
import json
from pathlib import Path
import re
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--before',action='store_true')
parser.add_argument('--work',type=Path,default=Path('/tmp/taxonomy-tunnel-interface/controls'))
a=parser.parse_args()
here=Path(__file__).resolve().parent
root=here.parents[3]
engine=root.parent/'cleave/target/release/cleave'
a.work.mkdir(parents=True,exist_ok=True)
ids=json.loads((here/'ids.json').read_text())
rules=list(ids if a.before else ids.values())
rules+=['objectives/exfiltration/messaging/webhook::webhook-with-system-data-host-2',
        'well-known/malware/rat/powershell-empire::empire-http-hop-session-proxy',
        'well-known/malware/rat/powershell-empire::empire-app-exploit-module']
config='interface tunnel 3\ntunnel source local\ntunnel destination remote\n'
texts={
 'empire-tun.ps1': '# ' + 'fixture padding ' * 20 + '\nfunction Exploit-JBoss { $device = "/dev/net/tun" }\n',
 'empire-spool-tun.ps1': '# ' + 'fixture padding ' * 20 + '\nfunction Invoke-SpoolSample { $device = "/dev/net/tun" }\n',
 'empire-signature-only.ps1': '# ' + 'fixture padding ' * 20 + '\nfunction Exploit-JBoss { return $null }\n',
 'tun.c': 'const char *device="/dev/net/tun";\nconst char *setup="TUNSETIFF";\n',
 'cisco.py': 'configuration = """'+config+'"""\n# webhook "ip": "192.0.2.1"\n',
 'cisco-far.py': 'configuration = """'+config+'"""\n# '+('X'*8192)+'\n# webhook "ip": "192.0.2.1"\n',
 'vpn.java': 'import android.net.VpnService;\nclass LocalTunnel extends VpnService { void configure() { new VpnService.Builder().addRoute("0.0.0.0", 0).addDisallowedApplication("org.example.local").addAllowedApplication("com.android.vending"); } }\n',
 'package.java': 'class Packages { String play = "com.android.vending"; String services = "com.google.android.gms"; }\n',
 'vpn.xml': '<config><class>Landroid/net/VpnService;</class><builder>Landroid/net/VpnService$Builder;</builder><route>addRoute</route><exclude>addDisallowedApplication</exclude></config>\n',
}
for name,text in texts.items():(a.work/name).write_text(text)
for name,full in [('wintun.dll',True),('wintun-reference.dll',False)]:
 target=a.work/name
 if target.exists():continue
 data=b'wintun.dll\0'+(b'tap0901\0' if full else b'')
 source=a.work/(name+'.c');obj=a.work/(name+'.obj')
 source.write_text('__declspec(dllexport) const unsigned char evidence[] = {'+','.join(map(str,data))+'};\n'+('__declspec(dllexport) int WintunCreateAdapter(void) { return 0; }\n' if full else ''))
 subprocess.run(['clang','--target=x86_64-pc-windows-msvc','-c',str(source),'-o',str(obj)],check=True,capture_output=True)
 subprocess.run(['lld-link','/dll','/noentry','/nodefaultlib','/opt:noref','/out:'+str(target),str(obj)],check=True,capture_output=True)
cases=list(texts)+['wintun.dll','wintun-reference.dll']
def scan(name):
 run=subprocess.run([str(engine),'--traits-dir',str(root),'test-rules','--rules',','.join(rules),str(a.work/name)],check=True,text=True,capture_output=True)
 (a.work/(name+('.before.log' if a.before else '.after.log'))).write_text(run.stdout+run.stderr)
 states={m[2].split('::')[-1]:[m[1],m[3]] for line in run.stdout.splitlines() if (m:=re.match(r'^(NOT MATCHED|MATCHED) (\S+) \((.*)\)',line))}
 assert len(states)==len(rules),(name,states,run.stdout[-2000:])
 return name,states
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:result=dict(pool.map(scan,cases))
for case,rule,yes in [('empire-tun.ps1','empire-app-exploit-module',True),('empire-spool-tun.ps1','empire-app-exploit-module',True),('empire-signature-only.ps1','empire-app-exploit-module',False),('tun.c','tun',True),('cisco.py','ios-tunnel-configuration-vocabulary',True),('cisco.py','webhook-with-system-data-host-2',True),('cisco-far.py','webhook-with-system-data-host-2',False),('vpn.java','android-vpn-application-exclusion-filter-source',True),('package.java','android-vpn-application-exclusion-filter-source',False),('wintun.dll','windows-virtual-tunnel-adapter',True),('wintun-reference.dll','windows-virtual-tunnel-adapter',False)]:
 assert (result[case][rule][0]=='MATCHED')==yes,(case,rule,result[case][rule])
baseline=here/'baseline.json'
if a.before:baseline.write_text(json.dumps(result,indent=2)+'\n')
else:assert result==json.loads(baseline.read_text()),json.dumps(result,indent=2)
print(f'{len(cases)} controls, {sum(map(len,result.values()))} rule verdicts verified'+(' and baseline saved' if a.before else ' against pre-move baseline'))
