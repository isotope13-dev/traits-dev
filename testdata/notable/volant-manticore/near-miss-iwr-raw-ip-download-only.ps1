# benign: raw IP health probe, response is only printed
$uri = "http://10.20.30.40:8080/health"
$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
Write-Output $response.StatusCode
