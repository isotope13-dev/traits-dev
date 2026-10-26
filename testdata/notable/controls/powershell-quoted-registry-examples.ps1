function Get-RegistryExamples {
    @'
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Example
New-ItemProperty -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -Name Example
Set-ItemProperty -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -Name Example
'@
}

function Show-LocalNotice {
    Start-Process pwsh -ArgumentList '-NoProfile','-Command','Write-Output ready' -WindowStyle Hidden -Wait
}
