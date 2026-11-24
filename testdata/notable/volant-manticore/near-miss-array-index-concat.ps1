$parts = "abc"
$name = $parts[0] + $parts[1] + 'x'
$req = [System.Net.WebRequest]::Create("https://example.org/")
$req.GetResponse() | Out-Null
