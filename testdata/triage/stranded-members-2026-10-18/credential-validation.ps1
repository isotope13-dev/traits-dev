do {
    $credential = Get-Credential
    $validCreds = $context.ValidateCredentials($credential.UserName, $credential.GetNetworkCredential().Password)
} while ($validCreds -eq $false -and $global:VerifyCreds -eq $true)
