$data = Invoke-WebRequest -Uri https://example.org/data.gz
$inputStream = New-Object System.IO.MemoryStream(, $data.Content)
$gzipStream = New-Object System.IO.Compression.GZipStream $inputStream, ([IO.Compression.CompressionMode]::Decompress)
$output = New-Object System.IO.MemoryStream
$gzipStream.CopyTo($output)
[IO.File]::WriteAllBytes("report.bin", $output.ToArray())
