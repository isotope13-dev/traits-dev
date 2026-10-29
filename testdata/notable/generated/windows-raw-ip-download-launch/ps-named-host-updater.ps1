(New-Object Net.WebClient).DownloadFile("https://downloads.example.com/app/setup.exe", "$env:TEMP\setup.exe")
Start-Process "$env:TEMP\setup.exe"
