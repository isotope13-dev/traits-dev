$SrcPath = 'C:\Temp\payload.exe'
$bytes = [IO.File]::ReadAllBytes($SrcPath)
$memory = New-Object IO.MemoryStream
$gzip = New-Object IO.Compression.GZipStream($memory, [IO.Compression.CompressionMode]::Compress)
$gzip.Write($bytes, 0, $bytes.Length)
$gzip.Dispose()
[IO.File]::WriteAllBytes('C:\Temp\stage.bin', $memory.ToArray())
