$bytes = [Security.Cryptography.RandomNumberGenerator]::GetBytes(24)
$token = [Convert]::ToBase64String($bytes) -replace '[+/=]', ''
Write-Output "token=$token"
