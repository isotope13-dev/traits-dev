function Invoke-EgressCheck
{
    param([String]$ip = '10.0.0.1', [String]$portrange = '80,443')
    foreach ($port in ($portrange -split ',')) {
        $t = New-Object System.Net.Sockets.TCPClient
        $t.BeginConnect($ip, [int]$port, $null, $null) | Out-Null
    }
}
