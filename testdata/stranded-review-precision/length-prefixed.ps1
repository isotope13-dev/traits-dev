$Length = [BitConverter]::ToInt64($Data, 0)
$Body = $Data[8..(7+$Length)]
[IO.File]::WriteAllBytes($OutputPath, $Body)
