$client = New-Object System.Net.WebClient
$client.DownloadFile("https://downloads.example.test/tool.exe", "$env:TEMP/tool.exe")
Start-Process "$env:TEMP/tool.exe" -Wait
