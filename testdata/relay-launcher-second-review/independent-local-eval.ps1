$client = New-Object System.Net.Sockets.TCPClient("127.0.0.1", 8888)
$stream = $client.GetStream()
$expression = "2 + 2"
Invoke-Expression $expression
$client.Close()
