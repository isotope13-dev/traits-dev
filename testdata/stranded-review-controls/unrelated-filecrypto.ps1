$transform = $aes.CreateDecryptor()
$bytes = [System.IO.File]::ReadAllBytes($inputPath)
[System.IO.File]::WriteAllBytes($outputPath, $transform.TransformFinalBlock($bytes, 0, $bytes.Length))
Remove-Item $scratchPath -Force
