$download = Join-Path $env:TEMP 'install_42.exe'
(New-Object System.Net.WebClient).DownloadFile('https://downloads.example.invalid/client.exe', $download); Start-Process $maintenance
