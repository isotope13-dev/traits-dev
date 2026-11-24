$client = New-Object System.Net.WebClient
$client.UploadString('https://example.invalid/log', 'test')
