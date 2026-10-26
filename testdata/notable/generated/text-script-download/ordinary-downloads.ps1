$client = New-Object System.Net.WebClient
$client.DownloadFile('https://cdn.invalid/report.txt', '%temp%\report.txt')
$client.DownloadFile('https://cdn.invalid/tool.vbs', 'C:\Tools\tool.vbs')
