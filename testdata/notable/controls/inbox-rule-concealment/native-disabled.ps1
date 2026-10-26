$headers = @{ Authorization = "Bearer $env:ACCESS_TOKEN" }
$uri = 'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules'
$folders = Invoke-RestMethod -Uri 'https://graph.microsoft.com/v1.0/me/mailFolders' -Headers $headers
$folder = ($folders.value | Where-Object displayName -eq 'Conversation History').id
$rules = @(
    @{ displayName = 'sss'; sequence = 1; isEnabled = $false
       conditions = @{}; actions = @{ markAsRead = $true; delete = $true } },
    @{ displayName = 'iT'; sequence = 2; isEnabled = $false
       actions = @{ moveToFolder = $folder; markAsRead = $true }; conditions = @{} }
)
foreach ($rule in $rules) {
    Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType 'application/json' -Body ($rule | ConvertTo-Json -Depth 4)
}
