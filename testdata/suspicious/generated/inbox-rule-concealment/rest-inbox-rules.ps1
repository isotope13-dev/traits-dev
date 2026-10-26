$headers = @{ Authorization = "Bearer $env:ACCESS_TOKEN" }
$uri = 'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules'
$body = @'
{"actions":{"delete":true,"markAsRead":true},"displayName":"cleanup","conditions":{},"sequence":1,"isEnabled":true}
'@
Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType 'application/json' -Body $body
$body = @'
{"actions":{"moveToFolder":"opaque-folder-id","markAsRead":true},"conditions":{},"sequence":2,"displayName":"archive","isEnabled":true}
'@
Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType 'application/json' -Body $body
