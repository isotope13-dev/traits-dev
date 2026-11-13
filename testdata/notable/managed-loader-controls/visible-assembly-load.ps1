# A visible, policy-respecting managed-code loader: same Assembly.Load
# primitive as the concealed stage, without the policy bypass or hidden
# window. The hostile composite must not fire; the reflective-load
# capability observation alone is expected.
param([string]$Path = "$PSScriptRoot\PlugIns\Hello.dll")
$bytes = [System.IO.File]::ReadAllBytes($Path)
$asm = [Reflection.Assembly]::Load($bytes)
& "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "[Reflection.Assembly]::Load([System.IO.File]::ReadAllBytes($Path)) | Out-Null"
Write-Host "loaded $($asm.FullName)"
