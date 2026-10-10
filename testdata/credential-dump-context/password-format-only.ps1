function CredManMain {
    $Cred = [pscustomobject]@{ CredentialBlob = 'example' }
    Write-Output @"
| Password | $($Cred.CredentialBlob)
"@
}
