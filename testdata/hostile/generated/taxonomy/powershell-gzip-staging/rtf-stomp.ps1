$bytes = [Text.Encoding]::UTF8.GetBytes('payload')
$memory = New-Object IO.MemoryStream
$gzip = New-Object IO.Compression.GZipStream($memory, [IO.Compression.CompressionMode]::Compress)
$gzip.Write($bytes, 0, $bytes.Length)
$gzip.Dispose()
$magic = '0x7B 0x5C 0x72 0x74 0x66'
[IO.File]::WriteAllBytes('C:\Temp\stage.rtf', $memory.ToArray())
