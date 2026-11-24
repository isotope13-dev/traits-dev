# Lists tEXt metadata of a local PNG file.
$bytes = [IO.File]::ReadAllBytes($args[0])
$i = 8
while ($i -lt $bytes.Length - 12) {
  $len = [BitConverter]::ToUInt32(($bytes[$i..($i+3)])[3..0], 0)
  $type = [Text.Encoding]::ASCII.GetString($bytes, $i + 4, 4)
  if ($type -eq 'tEXt') {
    Write-Output ([Text.Encoding]::ASCII.GetString($bytes, $i + 8, $len))
  }
  $i += $len + 12
  if ($type -eq 'IEND') { break }
}
