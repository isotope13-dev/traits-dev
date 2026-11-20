while ($true) {
    $client = New-Object System.Net.Sockets.TcpClient('45.92.111.116',8443)
    $stream = $client.GetStream()
    $record = "PING"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($record)
    $stream.Write($bytes,0,$bytes.Length)
    $client.Close()
    Start-Sleep -Seconds 60
}
