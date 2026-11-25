# Restart helper: spawns a detached hidden relaunch script through WMI.
function Restart-App([string]$Exe, [string]$Root) {
    $script = @"
Start-Sleep -Seconds 2
Start-Process '$Exe' -ArgumentList '"$Root"'
"@
    $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($script))
    $r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = "powershell.exe -NoProfile -WindowStyle Hidden -EncodedCommand $enc" }
    return ($r.ReturnValue -eq 0)
}
