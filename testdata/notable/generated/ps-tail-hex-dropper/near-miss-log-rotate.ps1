param([string]$LogFile, [int]$TailCount = 50)
$lines = [System.IO.File]::ReadAllLines($LogFile)
$recent = ($lines | Select-Object -Last $TailCount) -join "`n"
$cleanHex = $recent -replace '[^0-9A-Fa-f]', ''
$tmp = Join-Path $env:TEMP 'diag-export.txt'
[System.IO.File]::WriteAllBytes($tmp, [System.Text.Encoding]::UTF8.GetBytes($cleanHex))
$psi = New-Object System.Diagnostics.ProcessStartInfo('cmd.exe', '/c echo ok')
$p = [System.Diagnostics.Process]::Start($psi)
$p.WaitForExit()
Remove-Item $tmp -Force
