param($Panel,$ticket,$SessionId,$Command)
$headers = @{ Cookie = ".ASPXAUTH=$ticket" }
Invoke-RestMethod -Uri "$Panel/Services/PageService.ashx/GetLiveData" -Method Post -Headers $headers
$body = ConvertTo-Json @{EventType='QueuedCommand'; Data=$Command}
Invoke-RestMethod -Uri "$Panel/Services/PageService.ashx/AddSessionEvents" -Method Post -Headers $headers -Body $body
