$SrcPath = 'C:\Temp\payload.exe'
$bytes = [IO.File]::ReadAllBytes($SrcPath)

# Many unrelated setup steps separate the input reference from compression.
$a01 = 1
$a02 = 2
$a03 = 3
$a04 = 4
$a05 = 5
$a06 = 6
$a07 = 7
$a08 = 8
$a09 = 9
$a10 = 10
$a11 = 11
$a12 = 12
$a13 = 13
$a14 = 14
$a15 = 15
$a16 = 16
$a17 = 17
$a18 = 18
$a19 = 19
$a20 = 20
$a21 = 21
$a22 = 22
$a23 = 23
$a24 = 24
$a25 = 25
$a26 = 26
$a27 = 27
$a28 = 28
$a29 = 29
$a30 = 30
$a31 = 31
$a32 = 32
$a33 = 33
$a34 = 34
$a35 = 35
$memory = New-Object IO.MemoryStream
$gzip = New-Object IO.Compression.GZipStream($memory, [IO.Compression.CompressionMode]::Compress)
$gzip.Write($bytes, 0, $bytes.Length)
$gzip.Dispose()
[IO.File]::WriteAllBytes('C:\Temp\stage.bin', $memory.ToArray())
