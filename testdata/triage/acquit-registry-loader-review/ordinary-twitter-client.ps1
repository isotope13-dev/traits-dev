$endpoint = "http://api.twitter.com/1/statuses/user_timeline.xml?screen_name=$account"
$client = New-Object System.Net.WebClient
[xml] $reply = $client.DownloadString($endpoint)
$message = $reply.statuses.status.text
$action = $message.split('|')[0]
switch ($action) { !help { Write-Output $message }; !version { Get-Host } }
# An independent local configuration expression does not make feed text code.
Invoke-Expression $trustedExpression
