function Test-Login
{
    param([String]$URL, [String]$UserField, [String]$PassField)
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
    $r = Invoke-WebRequest -Uri $URL -Method POST -Body @{ $UserField = 'admin'; $PassField = 'secret' }
    return $r.Content -match 'Welcome'
}
function Test-Password { param([String]$p) Test-Login 'https://x/' 'u' $p }
