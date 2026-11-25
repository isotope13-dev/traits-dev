param([string]$Path)
$bytes = [Convert]::FromBase64String((Get-Content -Raw -Path $Path))
$input = New-Object System.IO.MemoryStream(,$bytes)
$out = New-Object System.IO.MemoryStream
$d = New-Object System.IO.Compression.DeflateStream($input, [System.IO.Compression.CompressionMode]::Decompress)
$d.CopyTo($out)
Set-Content -Path "$Path.out" -Value $out.ToArray() -AsByteStream
