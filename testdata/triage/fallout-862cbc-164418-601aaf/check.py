#!/usr/bin/env python3
"""Static controls; samples are read as data and are never executed."""
import json
import os
from pathlib import Path
import subprocess
import sys

samples = Path(sys.argv[1])
work = Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=True)
repo = Path(__file__).resolve().parents[3]
proc = 'objectives/exfiltration/stealer/system-info/process::powershell-beacon-process-query-http-post'
net = 'objectives/exfiltration/stealer/system-info/network::powershell-beacon-network-status-http-post'
wmic = 'micro-behaviors/process/info/commandline::powershell-wmic-commandline-query'
prop = 'micro-behaviors/process/info/commandline::powershell-process-commandline-property'
startup = 'micro-behaviors/data/db/web-storage::extension-startup-handler-storage-read'
space = 'micro-behaviors/communications/url/host/name::tld-space'
critical = 'micro-behaviors/process/control/critical::managed-break-on-termination-call-layout'
cases = []
def add(name, content, yes=(), no=()):
    path = work / name
    path.write_bytes(content.encode() if isinstance(content, str) else content)
    cases.append((path, set(yes), set(no)))

ps = (samples / '16441830473f/status.ps1').read_text()
add('beacon.ps1', ps, [proc, net, wmic], [prop])
add('diagnostics.ps1', ps.replace('beacon host cmdline', 'service process status'), [wmic], [proc, net, prop])
add('without-write.ps1', ps.replace('$s.Write($d,0,$d.Length);', ''), [wmic], [proc, net])
add('without-commandline.ps1', ps.replace('get CommandLine,', 'get Name,'), [net], [proc, wmic, prop])
add('without-netstat.ps1', ps.replace('netstat', 'route'), [proc, wmic], [net])
add('property.ps1', '(Get-Process -Id 123).CommandLine\n', [prop], [proc, net, wmic])
add('caption.ps1', 'Get-Process -Id 123\nWrite-Output "CommandLine"\n', [], [prop, wmic, proc, net])
js = 'chrome.runtime.onStartup.addListener(async()=>{await chrome.storage.local.get({enabled:false})});\n'
add('startup.js', js, [startup])
add('startup-write.js', js.replace('.get(', '.set('), [], [startup])
add('space.js', 'const endpoint="https://relay.example.space/path";\n', [space])
add('org.js', 'const endpoint="https://relay.example.org/path";\n', [], [space])
exe = (samples / '601aaf2d4f03/restaurantdupin.com_ransome.exe').read_bytes()
add('critical.exe', exe, [critical])
# Main RVA 0x2908; ldc.i4.s 29 at body offset 0x58d.
mut = bytearray(exe)
assert mut[0xb08 + 0x58d:0xb08 + 0x58f] == b'\x1f\x1d'
mut[0xb08 + 0x58e] = 28
add('class28.exe', mut, [], [critical])
mut = bytearray(exe)
assert mut[0xb08 + 0x580] == 0x17
mut[0xb08 + 0x580] = 0x16
add('false-flag.exe', mut, [], [critical])
assert b'NtSetInformationProcess\0' in exe
add('other-api.exe', exe.replace(b'NtSetInformationProcess\0', b'XtSetInformationProcess\0'), [], [critical])

run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo), '--format', 'json', *[str(p) for p, _, _ in cases]], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if run.returncode:
    raise SystemExit(run.stderr)
decoder = json.JSONDecoder()
remaining = run.stdout.strip()
reports = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].strip()
by_path = {f['path']: f for report in reports for f in report['files']}
checks = 0
for path, yes, no in cases:
    traits = {t['id']: t for t in by_path[str(path)]['traits']}
    assert yes <= traits.keys(), (path.name, 'missing', yes - traits.keys())
    assert not (no & traits.keys()), (path.name, 'unexpected', no & traits.keys())
    for old in ['objectives/exfiltration/http/collect::powershell-process-commandline-http-exfil', 'objectives/exfiltration/http/collect::powershell-network-status-http-exfil', 'objectives/supply-chain/hidden-payload/extensions/backdoor::extension-startup-handler-storage-read', 'objectives/command-and-control/infrastructure/domain/abused-tlds::tld-space']:
        assert old not in traits, (path.name, 'retired', old)
    for ident in (proc, net):
        if ident in traits:
            assert traits[ident]['crit'] == 4, (path.name, ident, 'must remain suspicious')
    checks += len(yes) + len(no) + 4
print(f'{len(cases)} static controls, {checks} assertions passed')
