$data = '{"tunnelModeTable":{"localVpnIp":"192.168.8.9; hostname; #"}}'
$method = "PUT"
Invoke-RestMethod -Uri "http://router.local/api/v1/network/ipsec" -Method $method -Body $data
