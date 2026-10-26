$input = New-Object IO.MemoryStream
$deflate = New-Object IO.Compression.DeflateStream($input, [IO.Compression.CompressionMode]::Decompress)
$gzip = New-Object IO.Compression.GZipStream($input, [IO.Compression.CompressionMode]::Decompress)
$reader = New-Object IO.StreamReader($gzip); $text = $reader.ReadToEnd()
