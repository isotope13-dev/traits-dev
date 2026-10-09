$d=[Convert]::FromBase64String("AAECAw==");$m=[Array]::ConvertAll($d,[System.Converter[byte,byte]]{param($x)$x-bxor250});[IO.File]::WriteAllBytes("output.bin",$m)
