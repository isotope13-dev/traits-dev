(New-Object Net.WebClient).DownloadFile("http://93.184.216.34/report.csv", "$env:TEMP\report.csv")
Start-Process notepad "$env:TEMP\report.csv"
