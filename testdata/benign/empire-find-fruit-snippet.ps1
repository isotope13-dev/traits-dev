function Find-Fruit
{
    param([String]$Rhosts, [Int]$Port = 8080)
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
    foreach ($h in ($Rhosts -split ',')) {
        try { (New-Object System.Net.WebClient).DownloadString("https://${h}:$Port/") } catch {}
    }
}
