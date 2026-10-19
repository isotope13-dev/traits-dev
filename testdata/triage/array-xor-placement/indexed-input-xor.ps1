param([byte[]]$InputBytes, [byte[]]$Mask)
$maskLength = $Mask.Length
$OutputBytes = New-Object 'System.Byte[]' $InputBytes.Length
for ($i = 0; $i -lt $InputBytes.Length; $i++) {
    $OutputBytes[$i] = $InputBytes[$i] -bxor $Mask[$i % $maskLength]
}
return $OutputBytes
