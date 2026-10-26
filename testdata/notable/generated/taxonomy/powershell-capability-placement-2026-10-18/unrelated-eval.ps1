$client = New-Object System.Net.WebClient
$page = $client.DownloadString('https://example.org/')
$local = 'Get-Date'
Invoke-Expression $local
