$response = Invoke-RestMethod -Uri "https://$Gateway/api/register" -Method Post -Body $payload
$assignedToken = $response.token
