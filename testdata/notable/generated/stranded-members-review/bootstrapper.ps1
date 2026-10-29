$installer = Join-Path $env:TEMP 'setup.exe'
(New-Object System.Net.WebClient).DownloadFile('https://downloads.example.invalid/setup.exe', $installer); Start-Process -FilePath $INSTALLER
