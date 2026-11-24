Invoke-WebRequest -Uri 'https://example.org/setup.ps1' -OutFile "$env:TEMP\setup.ps1" -UseBasicParsing
Start-Process -FilePath 'powershell.exe' -ArgumentList ('-File', "$env:TEMP\setup.ps1")
