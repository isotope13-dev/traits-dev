$headers = @{ Authorization = "Bearer $env:ACCESS_TOKEN" }
$uri = 'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules'
$folders = Invoke-RestMethod -Uri 'https://graph.microsoft.com/v1.0/me/mailFolders' -Headers $headers
$folder = ($folders.value | Where-Object displayName -eq 'Conversation History').id
$rules = @(
    @{ displayName = 'sss'; sequence = 1; isEnabled = $true
       conditions = @{}; actions = @{ notMarkAsRead = $true; delete = $true } },
    @{ displayName = 'iT'; sequence = 2; isEnabled = $true
       actions = @{ moveToFolder = $folder; notMarkAsRead = $true }; conditions = @{} }
)
foreach ($rule in $rules) {
    Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType 'application/json' -Body ($rule | ConvertTo-Json -Depth 4)
}
