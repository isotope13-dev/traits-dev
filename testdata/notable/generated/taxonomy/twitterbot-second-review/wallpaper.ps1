$temp = "$Env:temp"
$client.DownloadFile($url, $image)
Invoke-Expression 'rundll32.exe user32.dll, UpdatePerUserSystemParameters'

