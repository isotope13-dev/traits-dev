# benign: hostname origin, no IP literal
$uri = "https://packages.contoso.example/install.ps1"
$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
Invoke-Expression $response.Content
